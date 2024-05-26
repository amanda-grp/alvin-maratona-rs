import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


load_dotenv("config.env")
gemini_api_key = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(history=[])
chat
