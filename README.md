# mongo-import-export
mongo-import-export python


## Setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Usage

## Export Data
```
python app.py mongodb://root:root123@localhost:27017/db_name
```

## Import Data
```
python app.import.py ./db_name_1697789961.zip
```
