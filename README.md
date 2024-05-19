### Setup
1. Get Open AI API

2. Get Notion API

    Access https://www.notion.so/my-integrations.

    Click `+ New Integrations`.

    Enter some name and go ahead.

3. Setting in Notion

    Open tabs from the three dots in the upper right corner.

    Choose yous integrations from "Connect to".

    The name of the integration is the one entered in step 2.

4. Get Database ID
    In the same tab as in step 2, click on "Copy Link" and verify the database id.
    `https://www.notion.so/database_id?hoge`



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