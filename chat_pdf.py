import PyPDF2
from openai import OpenAI
import config as config

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

columns = config.columns

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def create_prompt():

    json_structure = '""""あなたは優秀な研究者です，日本語で要約してください, KeywordsはEnglish, 以下のフォーマットでできる限り最大限具体的に，参考文献はタイトル\n{\n'
    for column in columns:
        if column == "Keywords":
            json_structure += f'    "{column}": ["", ""]\n'
        else:
            json_structure += f'    "{column}": ,\n'
    json_structure += '}"""'

    return json_structure

def get_summary(pdf_path):
    pdf_text = read_pdf(pdf_path)

    prompt = create_prompt()

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