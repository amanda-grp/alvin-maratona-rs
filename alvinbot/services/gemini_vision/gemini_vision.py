import os
import re
import getpass
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv("config.env")
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")


def extract_validity_from_image(alert_image_url, current_date):
    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"""Analize essa imagem cuidadosamente e extraia o texto dela buscando pela vigência. 
                    Imprima as datas no formato: Vigência: DD/MM/YYYY hh:mm:ss até DD/MM/YYYY hh:mm:ss. Considere a data corrente {current_date}.""",
            },
            {
                "type": "image_url",
                "image_url": alert_image_url
            },
        ]
    )
    response = llm.invoke([message])
    return response.content

def extract_validity_from_text(text):


# print(extract_validity("https://www.defesacivil.rs.gov.br/upload/recortes/202405/24121131_71700_GDO.jpeg", "25/05/2024"))