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

    # 新しいページを追加するデータ
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": json_data['Name']
                        }
                    }
                ]
            },
            "どんなもの？": {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data['どんなもの？']
                        }
                    }
                ]
            },
            "先行研究と比較して新規性は？": {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data['先行研究と比較して新規性は？']
                        }
                    }
                ]
            },
            "手法のキモは？": {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data['手法のキモは？']
                        }
                    }
                ]
            },
            "有効性はどのように検証された？": {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data['有効性はどのように検証された？']
                        }
                    }
                ]
            },
            "課題と議論は？": {
                "rich_text": [
                    {
                        "text": {
                            "content": json_data['課題と議論は？']
                        }
                    }
                ]
            },
            "次に読む論文等は？": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(json_data['次に読む論文等は？'])
                        }
                    }
                ]
            },
            "Keywords": {
                "multi_select": keywords
            }
        }
    }

    # Notionのデータベースに新しいページを追加
    response = notion.pages.create(**new_page_data)

    # レスポンスを表示
    #print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and summarize arXiv paper")
    parser.add_argument("pdf_path", type=str, help="The pdf path want to make summarize")
    args = parser.parse_args()
    
    add_summary2notion(args.pdf_path)
