import os
import re
import getpass
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Tuple, Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class AlertBannerValidityExtractor:
    """
    This class retrieves the valid dates printed on the alert banners in the 
    website of the Defesa Civil of Rio Grande do Sul.
    """
    def __init__(self, current_date: Optional[datetime] = None):
        """
        Initializes the ValidityExtractor with the current date and loads the environment variables.

        :param current_date: The current date. If not provided, the current system date is used.
        """
        load_dotenv("config.env")

        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key: ")

        self.llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

        if current_date:
            self.current_date = current_date
        else:
            self.current_date = datetime.now()

    def extract_alerts_validities(self, images: List[str]) -> Tuple[List[dict], List[dict]]:
        """
        Extracts the validity of alerts from a list of images.

        :param images: A list of image URLs.
        :return: A tuple containing two lists of dictionaries. The first list contains valid alerts and the second list contains outdated alerts.
        """
        valid_alerts = []
        outdated_alerts = []

        for img_url in images:
            validity_text = self.extract_validity_from_image(img_url)
            start_date_str, end_date_str = AlertBannerValidityExtractor.extract_validity_from_text(validity_text)

            end_date = datetime.strptime(end_date_str, '%d/%m/%Y %H:%M:%S')

            if end_date > self.current_date:
                valid_alerts.append({img_url: (start_date_str, end_date_str)})
            else:
                outdated_alerts.append({img_url: (start_date_str, end_date_str)})

        return valid_alerts, outdated_alerts

    def extract_validity_from_image(self, alert_image_url: str) -> str:
        """
        Extracts the validity from an alert image.

        :param alert_image_url: The URL of the alert image.
        :return: The extracted validity text.
        """
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"""Analize essa imagem cuidadosamente e extraia o texto dela buscando pela vigência. 
                        Imprima as datas no formato: Vigência: DD/MM/YYYY hh:mm:ss até DD/MM/YYYY hh:mm:ss. 
                        Considere o ano corrente {self.current_date.year}.""",
                },
                {
                    "type": "image_url",
                    "image_url": alert_image_url
                },
            ]
        )
        response = self.llm.invoke([message])
        return response.content

    @staticmethod
    def extract_validity_from_text(text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the validity from a text.

        :param text: The text to extract the validity from.
        :return: A tuple containing the start date and end date.
        """
        pattern = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}"
        matches = re.findall(pattern, text)
        start_date = matches[0] if matches else None
        end_date = matches[1] if len(matches) > 1 else None

        return start_date, end_date
