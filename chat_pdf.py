import PyPDF2
from openai import OpenAI
import config as config

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def get_summary(pdf_path):
    pdf_text = read_pdf(pdf_path)

    prompt = "日本語で要約してください, KeywordsはEnglish, 以下のフォーマットで \
                {\
                    \"Name\": ,\
                    \"どんなもの？\": ,\
                    \"先行研究と比較して新規性は？\": ,\
                    \"手法のキモは？\": ,\
                    \"有効性はどのように検証された？\": ,\
                    \"課題と議論は？\": ,\
                    \"次に読む論文等は？\": ,\
                    \"Keywords\":[" ", ]\
                }"

    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."},
            {"role": "user", "content": pdf_text+"\n"+prompt}
        ]
        )
    except:
        print("An error occurred with ChatGPT")
        return None

    return completion.choices[0].message.content


if __name__ == "__main__":
    print(get_summary())