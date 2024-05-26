import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv("config.env")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

while True:
    prompt = input("Pergunte alguma coisa: ")
    if (prompt == "exit"):
        break
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        if chunk.text:
          print(chunk.text)