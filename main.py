from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import subprocess
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# papersディレクトリが存在しない場合は作成
if not os.path.exists('./papers'):
    os.makedirs('./papers')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-paper", response_class=HTMLResponse)
async def get_paper(request: Request, paper_id: str = Form(...)):
    # get_paper_by_id.pyを実行して結果を取得
    result = subprocess.run(
        ["python3", "get_paper_by_id.py", paper_id],
        capture_output=True,
        text=True,
        encoding='utf-8'  # ここでエンコーディングを指定
    )
    output = result.stdout.strip()
    
    # 結果表示ページのHTMLを作成
    return templates.TemplateResponse("result.html", {"request": request, "output": output})

@app.post("/upload-pdf", response_class=HTMLResponse)
async def upload_pdf(request: Request, pdf_file: UploadFile = File(...)):
    file_location = f"./papers/{pdf_file.filename}"
    with open(file_location, "wb") as file:
        file.write(pdf_file.file.read())
    result = subprocess.run(
        ["python3", "add_notion.py", file_location],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    output = result.stdout.strip()
    os.remove(file_location)

    return templates.TemplateResponse("result.html", {"request": request, "output": output})
