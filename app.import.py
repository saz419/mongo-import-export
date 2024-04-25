import pymongo
import json
from bson import json_util
import os
import zipfile
import sys
from urllib.parse import urlparse


def import_mongodb_data(mongo_uri, db_name, zip_file_path):
    try:
        client = pymongo.MongoClient(mongo_uri, connect=True)
        db = client[db_name]

        zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]
        exported_data_path = f'.unzipping/{zip_file_name}'
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(exported_data_path)

        json_files = [f for f in os.listdir(
            f'{exported_data_path}') if f.endswith('.json')]
        print("json_files: ", json_files)
        for json_file in json_files:
            collection_name = os.path.splitext(json_file)[0]

            with open(os.path.join(f'{exported_data_path}/', json_file), 'r') as file:
                data = json.load(file)
                # print(f'{json_file}: ', data)

            if isinstance(data, list):
                for document in data:
                    formatted_document = json_util.loads(
                        json_util.dumps(document))
                    db[collection_name].insert_one(formatted_document)
            else:
                db[collection_name].insert_one(data)

        print('Data has been imported into the MongoDB database')

        # # Delete the exported_data folder
        # shutil.rmtree(f'{exported_data_path}')

        # Close the MongoDB connection
        client.close()
    except Exception as err:
        print("Error Importing", err)


if __name__ == '__main__':
    mongo_uri = input("Enter mongo uri: ")
    uri_paths = urlparse(mongo_uri).path.split('/')
    db_name = uri_paths[1]
    print("Database: ", db_name)
    zip_file_path = sys.argv[1]
    import_mongodb_data(mongo_uri, db_name, zip_file_path)
