import unittest
import help_methods as HM
import credentials
import callybot_database

cred = credentials.Credentials()
token = cred.access_token
joachim_jahr_id = "1550995208259075"
db = callybot_database.CallybotDB(*cred.db_info)


class TestHelpMethods(unittest.TestCase):
    """Tests functions in help_method files"""

    def test_decrypt(self):
        """Tests encrypt and decrypt, and implicitly add_padding and remove_padding"""
        passwords = ["A", "Hei", "Vary", "Looong password, with_some|chars", "I guess this is enough?",
                     "Ill throw in a few extra weird chars",
                     "The next string are all the supported special chars on feide:",
                     " !#()*+,.=?@[]_{}~- "]
        for password in passwords:
            encrypted = HM.encrypt(password)
            decrypted = HM.decrypt(encrypted)
            self.assertEqual(password, decrypted)

    def test_get_course_exam_date(self):
        courses = (("kj2022", "2017-05-27"), ("TDT4140", ""), ("TDT4145", "2017-06-07"), ("TDT4180", "2017-06-02"),
                   ("TFY4125", "2017-05-30"), ("TTM4100", "2017-05-22"), ("IE502314", ""),
                   ("0", ""))
        for course, exam in courses:
            date = HM.get_course_exam_date(course)
            self.assertEqual(date, exam)

    def test_get_user_info(self):
        fname, lname, pic = HM.get_user_info(token, joachim_jahr_id)
        self.assertEqual("Joachim", fname)
        self.assertEqual("Jahr", lname)
        self.assertIn("https://scontent.xx.fbcdn.net/v/", pic)  # Checks that is https to picture on facebook

    def test_IL_scrape(self):
        queries = (("ALL", "31/12"), ("TDT4140", "31/12"), ("ALL", "1/5"), ("TDT4140", "1/5"))
        for course, date in queries:
            data = HM.IL_scrape(joachim_jahr_id, course, date, db)
            self.assertNotEqual(data, "SQLerror")
        self.assertEqual(HM.IL_scrape("00000", "ALL", "31/12", db), "SQLerror")

    def test_BB_scrape(self):
        queries = (("ALL", "31/12"), ("TDT4140", "31/12"), ("ALL", "1/5"), ("TDT4140", "1/5"))
        for course, date in queries:
            data = HM.BB_scrape(joachim_jahr_id, course, date, db)
            self.assertNotEqual(data, "SQLerror")
        self.assertEqual(HM.BB_scrape("00000", "ALL", "31/12", db), "SQLerror")

    def test_typo_correction(self):
        typo = HM.get_most_similar_command
        self.assertEqual(typo("zet reminder"), "set reminder")
        self.assertEqual(typo("het reminder"), "get reminder")
        self.assertEqual(typo("ramx"), "exam")
        self.assertEqual(typo("ramxs"), "exams")
        self.assertEqual(typo("subscribe anuncement"), "subscribe announcement")
        self.assertEqual(typo("halp"), "help")
        self.assertEqual(typo("help helap"), "help help")
        self.assertEqual(typo("hep get deafault.time"), "help get default-time")
        self.assertEqual(typo("developer announce"), "developer announcement")


if __name__ == '__main__':
    unittest.main()
