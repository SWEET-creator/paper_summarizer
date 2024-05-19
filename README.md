### Setup
1. Get Open AI API

2. Get Notion API

3. Setting in Notion

4. Get Database ID


### Create Config
rename config_dummy.py -> config.py
```
mv config_dummy.py config.py
```

Write apis and database ID in config.py.

### Excute
```
uvicorn main:app --reload
```

### Usage
Access http://127.0.0.1:8000.