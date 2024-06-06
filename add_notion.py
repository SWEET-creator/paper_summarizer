from notion_client import Client
from chat_pdf import get_summary
import config as config
import json
import re
import os
import argparse

# Notion APIキーを設定
notion = Client(auth=config.NOTION_API_KEY)

# データベースIDを設定
database_id = config.database_id

# カラム情報を設定
columns = config.columns

def add_summary2notion(pdf_path):
    plain_text = get_summary(pdf_path)
    
    if plain_text == None:
        return

    #print(plain_text)
    
    pattern = r'\{[^{}]+\}'

    # 正規表現を使ってマッチした部分を抽出
    matches = re.findall(pattern, plain_text)
    
    print(matches[0])
    
    json_data = json.loads(matches[0])
        
    keywords = [{"name" : keyword} for keyword in json_data['Keywords']]

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {},
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(json_data)
                            }
                        }
                    ]
                }
            }
        ]
    }

    for column in columns:
        if column == "Keywords":
            new_page_data["properties"][column] = {
                "multi_select": keywords
            }
        elif column == "Name":
            new_page_data["properties"][column] = {
                "title": [
                    {
                        "text": {
                            "content": json_data[column]
                        }
                    }
                ]
            }
        else:
            new_page_data["properties"][column] = {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data[column]
                        }
                    }
                ]
            }

    # Notionのデータベースに新しいページを追加
    response = notion.pages.create(**new_page_data)

    # レスポンスを表示
    #print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and summarize arXiv paper")
    parser.add_argument("pdf_path", nargs='?', default= "downloaded-paper.pdf", type=str, help="The pdf path want to make summarize")
    args = parser.parse_args()
    
    add_summary2notion(args.pdf_path)
