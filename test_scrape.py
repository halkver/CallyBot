import unittest
from iblack_scrape import scrape as BBscrape
from ilearn_scrape import scrape as ILscrape
from credentials import Credentials
from help_methods import decrypt
from reply import Reply as replyclass
from scraper import Scraper as scraperclass
from callybot_database import CallybotDB
from collections import deque

credentials = Credentials()
login_info = credentials.feide
access_token = credentials.access_token
database_creds = credentials.db_info
joachim_jahr_id = "1550995208259075"


class TestScraping(unittest.TestCase):
    def test_IL(self):
        successful = ILscrape(login_info[0], decrypt(login_info[1]))
        self.assertEqual(successful.__class__, list)
        unsuccessful = ILscrape("Invalid", "Invalid")
        self.assertEqual(unsuccessful, "error")

    def test_BB(self):
        successful = BBscrape(login_info[0], decrypt(login_info[1]))
        self.assertEqual(successful.__class__, list)
        unsuccessful = BBscrape("Invalid", "Invalid")
        self.assertEqual(unsuccessful, "error")

    def test_scraper(self):
        db = CallybotDB(*database_creds)
        replier = replyclass(access_token, db)
        scraper = scraperclass(replier, db)
        self.assertEqual(scraper.requests, deque([]))
        scraper.scrape(joachim_jahr_id, ["deadlines"])
        self.assertEqual(scraper.requests, deque([(joachim_jahr_id, ["deadlines"])]))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines"])), ("ALL", "31/12"))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines", "in", "tdt4140"])), ("tdt4140", "31/12"))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines", "until", "1/5"])), ("ALL", "1/5"))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines", "in", "tdt4140", "until", "1/5"])),
                         ("tdt4140", "1/5"))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines", "until", "1/5", "in", "tdt4140"])),
                         ("tdt4140", "1/5"))
        self.assertEqual(scraper.process((joachim_jahr_id, ["deadlines", "until", "1/5", "in", "tdt404"])),
                         ("tdt404", "1/5"))


if __name__ == '__main__':
    unittest.main()
