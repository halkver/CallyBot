import thread_settings
import credentials
import unittest


class Tester(unittest.TestCase):
    def setUp(self):
        self.settings = thread_settings.ThreadSettings(credentials.Credentials().access_token)

    def test_get_url(self):
        self.assertIn("https://graph.facebook.com/v2.8/me/thread_settings?access_token=",
                      self.settings.get_thread_url())

    def test_get_started(self):
        self.assertIn(b"Successfully", self.settings.set_get_started())

    def test_set_greeting(self):
        self.assertIn(b"Successfully", self.settings.set_greeting(
            "Hi there {{user_first_name}}!\nWelcome to CallyBot. Press 'Get Started' to get started!"))

    def test_persistent_menu(self):
        self.assertIn(b"Successfully", self.settings.set_persistent_menu())

    def test_whitelist(self):
        self.assertIn(b"Successfully", self.settings.whitelist("https://folk.ntnu.no/halvorkmTDT4140/"))


if __name__ == '__main__':
    unittest.main()
