import unittest
from datetime import datetime
from gemini_vision import AlertBannerValidityExtractor

class TestAlertBannerValidityExtractor(unittest.TestCase):
    def setUp(self):
        """
        Set up testing environment before each test.
        """
        self.validity_extractor = AlertBannerValidityExtractor(current_date=datetime(2024, 3, 26))

    def test_extract_validity_from_text(self):
        """
        Test extract_validity_from_text method.
        """
        text = "Vigência: 26/03/2024 00:00:00 até 27/03/2024 00:00:00"
        start_date, end_date = self.validity_extractor.extract_validity_from_text(text)
        self.assertEqual(start_date, "26/03/2024 00:00:00")
        self.assertEqual(end_date, "27/03/2024 00:00:00")

    def test_extract_validity_from_image_no_end_date(self):
        """
        Test extract_validity_from_image method when there is just an end time.
        """
        url = "https://www.defesacivil.rs.gov.br/upload/recortes/202405/24121131_71700_GDO.jpeg"
        valitdity_text = self.validity_extractor.extract_validity_from_image(url)
        self.assertEqual(valitdity_text, "Vigência: 25/05/2024 11:00:00 até 25/05/2024 11:00:00")

    def test_extract_validity_from_image_start_and_end_date(self):
        """
        Test extract_validity_from_image method when there is an start and end date.
        """
        url = "https://www.defesacivil.rs.gov.br/upload/recortes/202405/24181127_71797_GDO.jpeg"
        valitdity_text = self.validity_extractor.extract_validity_from_image(url)
        self.assertEqual(valitdity_text, "Vigência: 27/05/2024 00:00:00 até 28/05/2024 23:59:59")

    def test_extract_alerts_validities(self):
        """
        Test extract_alerts_validities method when there is an start and end date.
        """
        urls = ["https://www.defesacivil.rs.gov.br/upload/recortes/202405/24181127_71797_GDO.jpeg",
                "https://www.defesacivil.rs.gov.br/upload/recortes/202405/24121131_71700_GDO.jpeg"]
        
        valid_alert = [{urls[0]: ("27/05/2024 00:00:00", "28/05/2024 23:59:59")}]
        outdated_alert = [{urls[1]: ("25/05/2024 11:00:00", "25/05/2024 11:00:00")}]

        valid_alerts, outdated_alerts = self.validity_extractor.extract_alerts_validities(urls)
        self.assertEqual(valid_alerts, valid_alert)
        self.assertEqual(outdated_alert, outdated_alerts)