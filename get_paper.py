import os
import requests
import xml.etree.ElementTree as ET
from add_notion import add_summary2notion

def search_arxiv(keyword, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=all:{keyword}&start=0&max_results={max_results}'
    
    response = requests.get(base_url + query)
    response.raise_for_status()
    
    # Parse the XML response
    root = ET.fromstring(response.content)
    
    results = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        pdf_link = entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib['href']
        
        results.append({
            'title': title,
            'pdf_link': pdf_link
        })
    
    return results

def download_papers(papers, download_dir='./papers'):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    for paper in papers:
        title = paper['title'].replace(' ', '_').replace('/', '_')  # ファイル名として不適切な文字を置換
        pdf_link = paper['pdf_link']
        
        response = requests.get(pdf_link)
        response.raise_for_status()
        
        file_path = os.path.join(download_dir, f"{title}.pdf")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {title}")
        
        add_summary2notion(file_path)
    
        # PDFファイルを削除
        os.remove(file_path)
        print(f"Deleted: {file_path}")

# 使用例
keyword = "Image Generation"
max_results = 1
papers = search_arxiv(keyword, max_results)
download_papers(papers)
