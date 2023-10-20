import pymongo
import json
from bson import json_util, ObjectId
from datetime import datetime
import os
import zipfile
import shutil
import sys

def export_mongodb_data(mongo_uri, db_name):
    current_time = datetime.now()
    timestamp = int(current_time.timestamp())
    output_files_path = timestamp

    client = pymongo.MongoClient(mongo_uri, connect=True)
    db = client[db_name]
    collections = db.list_collections()

    os.makedirs(f'{output_files_path}')

    for collection in collections:
        collection_name = collection['name']

        data = list(db[collection_name].find({}))

        for document in data:
            if "_id" in document and not isinstance(document["_id"], ObjectId):
                document["_id"] = ObjectId(document["_id"])

        data = json.loads(json_util.dumps(data))
        with open(f'./{output_files_path}/{collection_name}.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

    client.close()

    zip_file_path = f'{db_name}_{output_files_path}.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(f'./{output_files_path}'):
            for file in files:
                file_path = os.path.join(root, file)
                arcName = os.path.relpath(file_path, f'{output_files_path}')
                zipf.write(file_path, arcName)

    print(f'Zip archive created at {zip_file_path}')

    # Delete the exported_data folder
    shutil.rmtree(f'{output_files_path}')


if __name__ == '__main__':
    mongo_uri = sys.argv[1]
    print(mongo_uri)
    db_name = input("Enter db name: ")
    export_mongodb_data(mongo_uri, db_name)
