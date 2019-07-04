from threading import Thread
from collections import deque
from time import sleep
from help_methods import IL_scrape, BB_scrape
import re


class Scraper(Thread):
    """The class inherits Thread, something that is necessary to make the Scraper start a new thread, which
    allows the server to send a '200 ok' fast after being prompted to scrape, and then scrape without facebook pushing
    new POST messages of the same get deadlines command.
    To add a scrape request to the queue, run function scrape(user_id, content_list)"""

    def __init__(self, reply_class, db):
        Thread.__init__(self)
        # Flag to run thread as a deamon (stops when no other threads are running)
        self.daemon = True
        self.requests = deque()
        self.pop = self.requests.popleft
        self.app = self.requests.append
        self.replier = reply_class

        self.course_code_format = "[0-9]?[æøåa-z]{1,6}[0-9]{1,6}[æøåa-z]{0,4}[0-9]{0,2}\-?[A-Z]{0,3}[0-9]{0,3}|mts/mo1"
        # Checks if string is in course_code format on ntnu
        date_format_separator = "[.,;:\\/-]"  # Date separators allowed. Regex format
        self.date_format = "(^(((0?[1-9]|1[0-9]|2[0-8])" + date_format_separator + "(0?[1-9]|1[012]))|((29|30|31)" + \
                           date_format_separator + "(0?[13578]|1[02]))|((29|30)" + date_format_separator + \
                           "(0?[469]|11))))"
        self.db = db

        self.rep = {"-": "/", "\\": "/", ":": "/", ";": "/", ",": "/", ".": "/"}
        # define desired replacements here.
        # Used in set reminder to get a standard format to work with
        self.rep = dict((re.escape(k), v) for k, v in self.rep.items())
        self.pattern = re.compile("|".join(self.rep.keys()))

    def run(self):
        while True:
            if self.requests:
                self.process(self.pop())
            else:
                sleep(2.5)  # Delay until looks again if it did not find an active scrape request

    def scrape(self, user_id, content_list):
        """Queues the scrape request for the server to handle"""
        self.app((user_id, content_list,))

    def process(self, query):
        """Scrapes Blackboard and It'slearning for deadlines"""
        user_id, content_list = query
        course = "ALL"
        until = "31/12"
        if len(content_list) == 1:  # Asks for all
            pass
        elif len(content_list) <= 3:  # Allows "in" and "until" to be dropped by the user
            if re.fullmatch(self.course_code_format, content_list[-1]):
                course = content_list[-1]
            elif re.fullmatch(self.date_format, content_list[-1]):
                until = content_list[-1]
            else:
                pass
        elif len(content_list) == 5:  # Strict format
            if content_list[1] == "in" and re.fullmatch(self.course_code_format, content_list[2]) and content_list[3] \
                    == "until" and re.fullmatch(self.date_format, content_list[4]):
                # Format: get deadline in aaa1111 until DD/MM
                course = content_list[2]
                until = content_list[4]
            elif content_list[1] == "until" and re.fullmatch(self.date_format, content_list[2]) and content_list[
                3] == "in" and re.fullmatch(self.course_code_format, content_list[
                4]):  # Format: get deadline until DD/MM deadline in aaa1111
                until = content_list[2]
                course = content_list[4]

        until = self.pattern.sub(lambda m: self.rep[re.escape(m.group(0))], until)
        # Makes any date string split with "/"

        IL_deadlines = IL_scrape(user_id, course, until, self.db)
        BB_deadlines = BB_scrape(user_id, course, until, self.db)
        if IL_deadlines == "SQLerror" or BB_deadlines == "SQLerror":
            self.replier.reply(user_id, "Could not fetch deadlines. Check if your user info is correct. You can "
                                        "probably fix this by using the 'login' command and logging in again with your"
                                        " feide username and password.\n\nIf you believe this is a bug, please report "
                                        "it with the 'bug' function", 'text')
        elif course == "ALL":
            IL_msg = "ItsLearning:\n" + IL_deadlines
            self.replier.reply(user_id, IL_msg, "text")
            BB_msg = "BlackBoard:\n" + BB_deadlines
            self.replier.reply(user_id, BB_msg, "text")
        else:
            if IL_deadlines or BB_deadlines:  # Both is returned as empty if does not have course
                self.replier.reply(user_id,
                                   "For course " + course.upper() + " I found these deadlines:\n"
                                   + IL_deadlines + BB_deadlines, "text")
            else:
                self.replier.reply(user_id, "I couldn't find any deadlines for " + course.upper(), "text")
        return course, until
