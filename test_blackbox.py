from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from collections import deque
import unittest


class FacebookTester(unittest.TestCase):
    """Tests the connection over facebook, login button, and a few commands"""

    def setUp(self):  # Start of each test
        """Initialize chat with cally"""
        options = webdriver.ChromeOptions()
        preferences = {"profile.default_content_setting_values.notifications": 2}  # Settings to remove pupups
        options.add_experimental_option("prefs", preferences)
        self.driver = webdriver.Chrome(chrome_options=options)  # Open Chrome with settings
        self.driver.get("http://www.facebook.com")
        elem = self.driver.find_element_by_id("email")
        elem.send_keys("jokki.reserve@gmail.com")
        elem = self.driver.find_element_by_id("pass")
        elem.send_keys("123abc123")
        elem.submit()
        # Login complete

        self.driver.get('https://www.facebook.com/messages/t/167935107030338')  # Direct link to chat with cally
        self.input_field = self.driver.find_element_by_class_name("_5rpu")  # Text field
        sleep(3)  # Let chat history load properly, can maybe be removed

    def tearDown(self):  # End of each test
        self.driver.close()

    def test_login(self):
        """Check if login button works"""
        logins_before_query = len(self.driver.find_elements_by_css_selector("._3cnp._3cnq"))
        # +1 due to message sent from tester
        self.input_field.send_keys("login")
        self.input_field.send_keys(Keys.ENTER)  # Simples way to send messages
        answers_before_query = len(self.driver.find_elements_by_css_selector("._3oh-._58nk"))
        answers_after_query = len(self.driver.find_elements_by_css_selector("._3oh-._58nk"))
        while answers_before_query == answers_after_query:  # Wait for answer
            sleep(.25)
            answers_after_query = len(self.driver.find_elements_by_css_selector("._3oh-._58nk"))
        sleep(1.5)  # Wait for button to load
        after_query = len(self.driver.find_elements_by_css_selector("._3cnp._3cnq"))
        self.assertEqual(logins_before_query + 1, after_query, "Login button did not appear")

    def test_some_question(self):
        """Writes some queries, and checks if answer is correct, requires that test user has default-time = 1 
        and courses = None"""
        queries = deque([(1, "start_new_chat"),  # 1
                         (1, "get default-time"),
                         (1, "set default-time 2"),
                         (1, "get default-time"),
                         (1, "set default-time 1"),  # 5
                         (1, "get exams"),
                         (1, "GeT ExAmS"),
                         (1, "subscribe"),
                         (3, "subscribe TTM4100 TDT404"),
                         (1, "get exams"),  # 10
                         (3, "unsubscribe TTM4100 TDT404")])
        # Swapped to correspond to queries
        answers = deque(
            ["Welcome Joachim!\nMy name is CallyBot, but you may call me Cally \nI will keep you up to "
             "date on your upcoming deadlines on itslearning and Blackboard. Type 'Login' "
             "or use the menu next to the chat area to get started. "
             "\nIf you need help, or want to know more "
             "about what I can do for you, just type 'Help'.\n\nPlease do enjoy!",  # 1

             "Your default-time is: 1 day(s)",

             "Your default-time was set to: 2 day(s).\nTo update your deadlines "
             "to fit this new default-time, write "
             "'Get deadlines' or select the "
             "'Get deadlines' option"
             " from the menu next to the chat area.",

             "Your default-time is: 2 day(s)",

             "Your default-time was set to: 1 day(s).\nTo update your deadlines "
             "to fit this new default-time, write "
             "'Get deadlines' or select the "
             "'Get deadlines' option"
             " from the menu next to the chat area.",

             "I could not find any exam dates, are you sure you are subscribed to any courses?",

             "I could not find any exam dates, are you sure you are subscribed to any courses?",

             "Please specify what to subscribe to. Type 'Help' or visit "
             "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands",

             "Subscribing to TTM4100, TDT404...", "The following course(s) do(es) not exist: TDT404",
             "You have successfully subscribed to TTM4100",

             "The exam in TTM4100 is on 2017-05-22",  # 10

             "Unsubscribing from TTM4100, TDT404...", "The following course(s) do(es) not exist: TDT404",
             "You have successfully unsubscribed from TTM4100"])
        next_question = queries.popleft
        next_answer = answers.popleft
        while queries:  # Ask and check while there are queries left
            number, question = next_question()
            self.input_field.send_keys(question)
            self.input_field.send_keys(Keys.ENTER)  # Simples way to send messages
            sent = True  # Wait for answer
            seen = len(self.driver.find_elements_by_css_selector("._3oh-._58nk"))  # This is the class name for
            # single messages, but accessed with css selector due to having spaces in the name
            while sent:
                new_elems = self.driver.find_elements_by_css_selector("._3oh-._58nk")
                now_amount = len(new_elems)  # Number of current messeges in chat
                if seen + number == now_amount:  # If there are any new messages
                    for nr in range(seen, now_amount):
                        expected = next_answer()
                        self.assertEqual(new_elems[nr].text, expected, "Failed at query: " + question)
                    sent = False  # Tester should send next question
                else:
                    sleep(.1)  # Waiting time in pooling. in sec


if __name__ == '__main__':
    unittest.main()
