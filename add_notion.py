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
    #plain_text = get_summary(pdf_path)
    plain_text = """
                    { "Name": "High-Resolution Image Synthesis with Latent Diffusion Models", "どんなもの？": "この研究は、効率的で高品質な高解像度画像生成を目指して、潜在空間に基づく拡散モデル（LDM）を提案しています。", "先行研究と比較して新規性は？": "従来の拡散モデルがピクセル空間で動作していたのに対し、本研究は高解像度での画像生成を行うために、潜在空間で拡散モデルを動作させる点が新規です。", "手法のキモは？": "まず、有力な事前訓練されたオートエンコーダを使用して、画像を低次元の潜在空間に圧縮します。その後、この潜在空間で拡散モデルを訓練します。また、クロスアテンション層を導入し、一般的な条件付け入力を受け付ける柔軟なモデルを構築します。", "有効性はどのように検証された？": "提案したLDMは、画像補完、クラス条件付き画像生成、テキスト条件付き画像生成、超解像など様々なタスクで最先端の手法と比較して高い性能を示しました。また、従来のモデルと比べて計算効率が大幅に向上しました。", "課題と議論は？": "生成した画像の質は高いが、GANのような速度はまだ達成されていません。また、潜在空間の再構成能力は、ピクセルレベルの精度を要求されるタスクには制約があります。", "次に読む論文等は？": "分類器フリー拡散誘導、他の条件付き生成タスクへの応用、GANと拡散モデルの融合に関する研究。", "Keywords": ["Latent Diffusion Models", "High-Resolution Image Synthesis", "Denoising Autoencoders", "Cross-Attention"] }
                """
    
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
