import arxiv
from add_notion import add_summary2notion
import os
import argparse

def download_and_summarize_paper(arxiv_id, dirpath="./papers", filename="downloaded-paper.pdf"):
    file_path = os.path.join(dirpath, filename)
    paper = next(arxiv.Client().results(arxiv.Search(id_list=[arxiv_id])))
    paper.download_pdf(dirpath=dirpath, filename=filename)
    add_summary2notion(file_path)
    os.remove(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and summarize arXiv paper")
    parser.add_argument("arxiv_id", type=str, help="The arXiv ID of the paper to download and summarize")
    args = parser.parse_args()
    
    download_and_summarize_paper(args.arxiv_id)
