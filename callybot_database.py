import MySQLdb
from datetime import datetime, timedelta
from help_methods import IL_scrape, BB_scrape


class CallybotDB:
    """Class object for access to Callybot's MySQL database"""

    def __init__(self, host, username, password, DB_name):
        """Initializes CallybotDB, sets up connection to the database"""
        self.host, self.username, self.password, self.DB_name = host, username, password, DB_name
        self.db = None
        self.cursor = None
        self.init_time = datetime.now()
        self.open()

    def open(self):
        """open connection to database, void"""
        print("trying to connect to " + self.host)
        try:
            self.db = MySQLdb.connect(self.host, self.username, self.password, self.DB_name)
        except MySQLdb.OperationalError:
            print("\n\n\n\n\n\n\n\n\n\n####################################################\nServer could not "
                  "connect to database. Fatal error\nTime alive: ", datetime.now() - self.init_time, "\n\nFrom: ",
                  self.init_time, "\nTo: ", datetime.now(), "\n####################################################")
            raise SystemExit  # Terminates entire bot
        self.cursor = self.db.cursor()
        print("successful connect to database " + self.DB_name)

    def close(self):
        """close connection to database, void"""
        self.db.close()

    def test_connection(self):
        """Tests if connection with server is still live, if it is not it tries to open a new connection, void"""
        try:
            if self.db.stat() == "MySQL server has gone away":
                self.close()
                self.open()
        except MySQLdb.OperationalError:
            try:
                self.close()
            except MySQLdb.ProgrammingError:  # Already closed
                pass
            self.open()

    def get_credential(self, user_id):
        """Get all saved information about a user,
        :returns a list [fbid, username, password, defaulttime, announcement]"""
        self.test_connection()
        self.db.commit()
        sql = "SELECT * FROM user WHERE fbid=" + str(user_id)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results[0] if results else []

    def add_user(self, user_id, username=None, password=None, df=1, announcement=1):
        """Add a user to the database
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        if username is None or password is None:
            sql = "INSERT INTO user(fbid, defaulttime, announcement)" \
                  " VALUES('%s', '%d', '%d')" % (user_id, df, announcement)
        else:
            sql = "INSERT INTO user(fbid, username, password, defaulttime, announcement)" \
                  " VALUES('%s', '%s', '%s', '%d', '%d')" % (user_id, username, password, df, announcement)
        if not self.user_exists(user_id):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def remove_user(self, user_id):
        """Deletes a user from the database
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        if self.user_exists(user_id):
            sql = """DELETE FROM user WHERE fbid=""" + str(user_id)
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def user_exists(self, user_id):
        """Checks if a user is already in the database,
        :returns Boolean value"""
        self.test_connection()
        sql = """SELECT * FROM user WHERE fbid=""" + str(user_id)
        result = self.cursor.execute(sql)
        return result != 0

    def get_user_ids(self):
        """:returns all existing users' fbid as a list"""
        self.test_connection()
        sql = """SELECT fbid FROM user"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def set_username_password(self, user_id, username, password):
        """Sets username and password for a user that already exists
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        sql = """UPDATE user SET username='%s', password='%s' WHERE fbid='%s'""" % (username, password, user_id)
        if self.user_exists(user_id):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def add_course(self, course_code, course_name):
        """Adds course to database if it does not already exist
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        sql = """INSERT INTO course(coursecode, courseName) VALUES ('%s', '%s')""" % (course_code, course_name)
        if not self.course_exists(course_code):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def remove_course(self, course):
        """Deletes course from the database if it is in the database
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        sql = """DELETE FROM course WHERE coursecode='%s'""" % str(course)
        if self.course_exists(course):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def course_exists(self, course):
        """Checks if a course is in the database,
        :returns Boolean value"""
        self.test_connection()
        sql = "SELECT * FROM course WHERE coursecode = %s"
        result = self.cursor.execute(sql,(course,))
        return result != 0

    def subscribe(self, user_id, course):
        """Creates a relation between course and user in table subscribed if the relation does not already exist,
         assumes both course and user is already in the database
         :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        sql = """INSERT INTO subscribed (userID, course) VALUES ('%s', '%s')""" % (user_id, course)
        if not (self.user_subscribed_to_course(user_id, course)) and self.user_exists(user_id) and self.course_exists(
                course):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def user_subscribed_to_course(self, user_id, course):  # unit tested
        """Checks if a user is subscribed to a course,
        :returns Boolean value"""
        self.test_connection()
        sql = """SELECT * FROM subscribed
                WHERE userID='%s' AND course='%s'""" % (user_id, course)
        result = self.cursor.execute(sql)
        return result != 0

    def unsubscribe(self, user_id, course):
        """Deletes the relation between user and course if the relation exists
        :returns whether sql was successful or not"""
        self.test_connection()
        result = 0
        sql = """DELETE FROM subscribed
                WHERE userID='%s' AND course='%s'""" % (user_id, course)
        if self.user_subscribed_to_course(user_id, course):
            result = self.cursor.execute(sql)
            self.db.commit()
        return result

    def add_reminder(self, what, deadline, coursemade, user_id):
        """Add reminder to the database,
        what: <String> whatever user wants to be reminded of,
        deadline: <'YYYY-MM-DD HH:MM'> whenever user wants to be reminded of it,
        coursemade: <Boolean> True if this reminder is an assignment, False if costum reminder,
        user_id: <String> the user who wants to reminded of what,
        :returns whether sql was successful or not"""
        result = 0
        if self.user_exists(user_id):
            self.test_connection()
            # change the deadline specified by the defaulttime
            # only alter deadline if coursemade == 1
            new_deadline = deadline
            if coursemade:
                df = self.get_defaulttime(user_id)
                new_deadline = fix_new_deadline(deadline, df)
            sql = "INSERT INTO reminder(what, deadline, userID, coursemade) " \
                  "VALUES (%s, %s, %s, %s)" #% (what, new_deadline, user_id, coursemade)
            result = self.cursor.execute(sql,(what, new_deadline, user_id, coursemade))
            self.db.commit()
        return result

    def get_defaulttime(self, user_id):
        """:returns a users defaulttime <Integer>. 0 if user does not exist"""
        # gets the defaulttime set by the user of how long before a deadline the user wish to reminded of it
        self.test_connection()
        sql = """SELECT defaulttime FROM user WHERE fbid='%s'""" % user_id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result[0][0] if result else 0

    def set_defaulttime(self, user_id, df):
        """Sets a user's defaulttime to be df <Integer>
        :returns True if query completed"""
        self.test_connection()
        try:
            sql = """UPDATE user SET defaulttime=%d WHERE fbid='%s'""" % (df, user_id)
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except MySQLdb.OperationalError:
            return False

    def unsubscribe_announcement(self, user_id):
        """Sets announcement field in user table to 0 if user was subscribed to announcements
        :returns True if query completed"""
        self.test_connection()
        if not self.subscribed_to_announcement(user_id):
            return False
        try:
            sql = """UPDATE user SET announcement='0' WHERE fbid='%s'""" % user_id
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.OperationalError:
            return False
        return True

    def subscribe_announcement(self, user_id):
        """Sets announcement field in user table to 1 if user was not subscribed to announcements
        :returns True if query completed"""
        self.test_connection()
        if self.subscribed_to_announcement(user_id):
            return False
        try:
            sql = """UPDATE user SET announcement='1' WHERE fbid='%s'""" % user_id
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.OperationalError:
            return False
        return True

    def subscribed_to_announcement(self, user_id):
        """:returns <Boolean> whether a user is subscribed to announcements"""
        self.test_connection()
        sql = """SELECT announcement from user WHERE fbid='%s'""" % user_id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return int(result[0][0])

    def clean_course(self, user_id):
        """Deletes all relations a user has to its courses
        :returns whether sql was successful or not"""
        # this is possibly quicker than just calling unsubscribe for all courses a user has
        self.test_connection()
        sql = """DELETE FROM subscribed WHERE userID='%s'""" % str(user_id)
        result = self.cursor.execute(sql)
        self.db.commit()
        return result

    def get_all_courses(self, user_id):
        """returns all courses a user is subscribed to,
        :returns a list of courses,
        [] (empty list) if a user is not subscribed to any courses"""
        self.test_connection()
        sql = """SELECT course FROM subscribed WHERE userID='%s'""" % user_id
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        # results is now a list of lists only containing the coursecode [[coursecode],]
        return [row[0] for row in results]

    def get_reminders(self, user_id):
        """:returns all reminders a user has format: ((what, deadline, coursemade, RID),...)"""
        self.test_connection()
        sql = """SELECT what, deadline, coursemade, RID FROM reminder
                        WHERE userID='%s' ORDER BY deadline ASC""" % user_id
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def delete_all_reminders(self, user_id):
        """Deletes all reminders a user has
        :returns whether sql was successful or not"""
        self.test_connection()
        sql = """DELETE FROM reminder
                        WHERE userID='%s'""" % user_id
        result = self.cursor.execute(sql)
        self.db.commit()
        return result

    def delete_all_coursemade_reminders(self, user_id):
        """Deletes all reminders that are coursemade for a user_id
        :returns whether sql was successful or not"""
        self.test_connection()
        sql = """DELETE FROM reminder
                        WHERE userID='%s' AND coursemade = 1""" % user_id
        result = self.cursor.execute(sql)
        self.db.commit()
        return result

    def delete_reminder(self, rid):
        """Deletes reminder with this rid
        :returns whether sql was successful or not"""
        self.test_connection()
        sql = """DELETE FROM reminder
                        WHERE RID='%s'""" % rid
        result = self.cursor.execute(sql)
        self.db.commit()
        return result

    def get_all_reminders(self):
        """Returns all reminders in the database,
        :returns ((deadline, userID, what, coursemade, RID),...)"""
        self.test_connection()
        sql = """SELECT deadline, userID, what, coursemade, RID FROM reminder"""
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def get_announcement_subscribers(self):
        """:returns a list of users subscribed to announcements"""
        self.test_connection()
        sql = """SELECT fbid FROM user WHERE announcement='1'"""
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return [row[0] for row in results]


def fix_new_deadline(deadline, df):
    """:returns deadline minus df days"""
    # deadline is supposed to be a string of format 'YYYY-MM-DD HH:MM:SS'
    return (datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S") - timedelta(days=df)).strftime("%Y-%m-%d %H:%M:%S")
