import unittest
import server_main


class ServerMainTester(unittest.TestCase):
    """Tests the connection over facebook, login button, and a few commands"""

    def test_init(self):
        self.assertIn(b"Successfully", server_main.init())

    def test_check_reminders(self):
        self.assertEqual(list, server_main.reminder_check().__class__)


if __name__ == '__main__':
    unittest.main()
