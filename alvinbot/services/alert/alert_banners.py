import os
import csv
import requests
from typing import List
from bs4 import BeautifulSoup
from urllib.request import urlopen
# from apscheduler.schedulers.blocking import BlockingScheduler

from alvinbot.services.vision.gemini_vision import AlertBannerValidityExtractor


class AlertBannersURLExtractor:
    def __init__(self):
        """Initialize the AlertBannersURLExtractor."""
        self.root_url = 'https://www.defesacivil.rs.gov.br'
        self.knowled_base_path = os.path.join('data', 'tables', 'Real_ListaDeAlertasEmRS.csv')
        self.validity_extractor = AlertBannerValidityExtractor()

    def get_alert_banners_urls(self) -> List[str]:
        """Get the URLs of alert banners.

        Returns:
            list: A list of URLs of alert banners.
        """
        alerts_urls = []
        htmldata = urlopen(f'{self.root_url}/inicial')
        soup = BeautifulSoup(htmldata, 'html.parser')
        images = soup.find_all('img')

        for item in images:
            image = item['src']
            if image.startswith('/upload/recortes/') and '_TH' in image:
                alerts_urls.append(f'{self.root_url}{image}')

        return alerts_urls
    
    def extract_alerts_validities(self, write_result=True) -> List[dict]:
        """Extract the validities of alerts.

        Args:
            write_result (bool, optional): Whether to write the result to a CSV file. Defaults to True.

        Returns:
            list: A list of dictionaries containing the URL, start date, end date, and validity of each alert.
        """
        images_urls = self.get_alert_banners_urls()
        valid_alerts, outdated_alerts = self.validity_extractor.extract_alerts_validities(images_urls)

        alerts_urls = []
        for alert in valid_alerts:
            alert_url = list(alert.keys())[0]
            alert_dates = list(alert.items())[0][1]
            alerts_urls.append({"url": alert_url, "data_inicio": alert_dates[0], "data_fim": alert_dates[1], "esta_expirado": True})

        for alert in outdated_alerts:
            alert_url = list(alert.keys())[0]
            alert_dates = list(alert.items())[0][1]
            alerts_urls.append({"url": alert_url, "data_inicio": alert_dates[0], "data_fim": alert_dates[1], "esta_expirado": False})
    
        if write_result:
            self.write_to_csv(alerts_urls)

        return alerts_urls

    def read_from_csv(self) -> List[dict]:
        """Read data from a CSV file.

        Returns:
            list: A list of dictionaries containing the data from the CSV file.
        """
        data = []
        try:
            with open(self.knowled_base_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            pass  # File doesn't exist yet, will be created by write_to_csv
        return data

    def write_to_csv(self, alerts_urls: List[str]) -> None:
        """Write data to a CSV file.

        Args:
            alerts_urls (list): A list of dictionaries containing the URL, start date, end date, and validity of each alert.
        """
        fieldnames = ["url", "data_inicio", "data_fim", "esta_expirado"]
        existing_alerts = self.read_from_csv()

        with open(self.knowled_base_path, mode='w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for alert in alerts_urls:
                if alert not in existing_alerts:
                    existing_alerts.append(alert)

                writer.writerow(alert)
        
    @staticmethod
    def download_image(url: str, target_dir: str) -> None:
        """Download an image.

        Args:
            url (str): The URL of the image.
            target_dir (str): The directory where the image will be saved.
        """
        filename = os.path.join(target_dir, url.split('/')[-1])
        response = requests.get(url)

        with open(filename, 'wb') as file:
            file.write(response.content)


def job():
    """The job that will be run every 15 minutes."""
    alert_extractor = AlertBannersURLExtractor()
    alert_extractor.extract_alerts_validities()

# # Schedule the job
# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'interval', minutes=15)
# scheduler.start()
