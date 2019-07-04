import reply
import credentials
import unittest
import callybot_database
from datetime import datetime, timedelta

credential = credentials.Credentials()
db = callybot_database.CallybotDB(*credential.db_info)
replier = reply.Reply(credential.access_token, db)


class Tester(unittest.TestCase):
    def test_process_data(self):
        test_data_message = {
            'entry': [{'messaging': [{'message': 'this is message'}]}]}  # check for message not text or attachment
        data_type, content = reply.Reply.process_data(test_data_message)
        self.assertEqual(data_type, "unknown")
        self.assertEqual(content, "")

        test_data_text = {'entry': [{'messaging': [{'message': {'text': 'this is text'}}]}]}  # check for text string
        data_type, content = reply.Reply.process_data(test_data_text)
        self.assertEqual(data_type, "text")
        self.assertEqual(content, "this is text")

        test_data_type = {'entry': [
            {'messaging': [{'message': {'attachments': [{'type': 'this is a type'}]}}]}]}  # check for nonexistent type
        data_type, content = reply.Reply.process_data(test_data_type)
        self.assertEqual(data_type, "unknown")
        self.assertEqual(content, "")

        test_data_image = {'entry': [{'messaging': [{'message': {
            'attachments': [{'type': 'image', 'payload': {'url': 'this is image url'}}]}}]}]}  # check for image
        data_type, content = reply.Reply.process_data(test_data_image)
        self.assertEqual(data_type, "image")
        self.assertEqual(content, "this is image url")

        test_data_video = {'entry': [{'messaging': [{'message': {
            'attachments': [{'type': 'video', 'payload': {'url': 'this is video url'}}]}}]}]}  # check for video
        data_type, content = reply.Reply.process_data(test_data_video)
        self.assertEqual(data_type, "video")
        self.assertEqual(content, "this is video url")

        test_data_file = {'entry': [{'messaging': [{'message': {
            'attachments': [{'type': 'file', 'payload': {'url': 'this is file url'}}]}}]}]}  # check for file
        data_type, content = reply.Reply.process_data(test_data_file)
        self.assertEqual(data_type, "file")
        self.assertEqual(content, "this is file url")

        test_data_audio = {'entry': [{'messaging': [{'message': {
            'attachments': [{'type': 'audio', 'payload': {'url': 'this is audio url'}}]}}]}]}  # check for audio
        data_type, content = reply.Reply.process_data(test_data_audio)
        self.assertEqual(data_type, "audio")
        self.assertEqual(content, "this is audio url")

        test_data_multimedia = {'entry': [{'messaging': [{'message': {
            'attachments': [{'type': 'multimedia', 'payload': 'this is multimedia url'}]}}]}]}  # check for multimedia
        data_type, content = reply.Reply.process_data(test_data_multimedia)
        self.assertEqual(data_type, "multimedia")
        self.assertEqual(content, "this is multimedia url")

        test_data_geolocation = {'entry': [{'messaging': [{'message': {'attachments': [
            {'type': 'geolocation', 'payload': 'this is geolocation url'}]}}]}]}  # check for geolocation
        data_type, content = reply.Reply.process_data(test_data_geolocation)
        self.assertEqual(data_type, "geolocation")
        self.assertEqual(content, "this is geolocation url")

        test_data_quick_reply = {'entry': [{'messaging': [
            {'message': {'quick_reply': {'payload': "this is reply"},
                         'text': 'this is text'}}]}]}  # check for quick reply
        data_type, content = reply.Reply.process_data(test_data_quick_reply)
        self.assertEqual(data_type, "text")
        self.assertEqual(content, "this is reply")

    def test_arbitrate(self):
        test_id = "123456789"

        test_text = {'entry': [{'messaging': [
            {'message': {'text': 'yes, i agree to delete all my information'}}]}]}  # check for text string
        msg = "I have now deleted all your information. If you have any feedback to give me, please " \
              "do so with the 'Request' command.\nI hope to see you again!"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'hello'}}]}]}  # check for text string
        msg = "http://cdn.ebaumsworld.com/mediaFiles/picture/2192630/83801651.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'hi'}}]}]}  # check for text string
        msg = "http://cdn.ebaumsworld.com/mediaFiles/picture/2192630/83801651.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'juice gif'}}]}]}  # check for text string
        msg = "https://i.makeagif.com/media/10-01-2015/JzrY-u.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'juicy gif'}}]}]}  # check for text string
        msg = "http://68.media.tumblr.com/tumblr_m9pbdkoIDA1ra12qlo1_400.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'who are you?'}}]}]}  # check for text string
        msg = "https://folk.ntnu.no/halvorkm/callysavior.jpg"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'who am i?'}}]}]}  # check for text string
        msg = ":)"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'good bye'}}]}]}  # check for text string
        msg = "http://i.imgur.com/NBUNSSG.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'rick'}}]}]}  # check for text string
        msg = "https://media.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'image')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'start_new_chat'}}]}]}  # check for text string
        msg = "Welcome Does not!\nMy name is CallyBot, but you may call me Cally :)\nI will keep you up to " \
                                       "date on your upcoming deadlines on itslearning and Blackboard. Type 'Login' " \
                                       "or use the menu next to the chat area to get started. " \
                                       "\nIf you need help, or want to know more " \
                                       "about what I can do for you, just type 'Help'.\n\nPlease do enjoy!"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'most_likely_command_was_not_true'}}]}]}  # check for text string
        msg = "I'm sorry I was not able to help you. Please type 'Help' to see my supported commands, or 'Help " \
              "<feature>' to get information about a specific feature, or visit my " \
              "wiki https://github.com/Folstad/TDT4140/wiki/Commands.\nIf you believe you found a bug, or have a " \
              "request for a new feature or command, please use the 'Bug' and 'Request' commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'developer something'}}]}]}  # check for text string
        msg = "Sorry, but these commands are only for developers. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get'}}]}]}  # check for text string
        msg = "Please specify what to get. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get deadlines'}}]}]}  # check for text string
        msg = "I'll go get your deadlines right now. If there are many people asking for deadlines this might take me some time."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get profile'}}]}]}  # check for text string
        msg = "Hello Does not Exist!\nYou are not subscribed to any courses\nYou do not have any active reminders"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get reminders'}}]}]}  # check for text string
        msg = "You don't appear to have any reminders scheduled with me"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get exams'}}]}]}  # check for text string
        msg = "I could not find any exam dates, are you sure you are subscribed to any courses?"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get exam TDT4145'}}]}]}  # check for text string
        msg = "The exam in tdt4145 is on 2017-06-07\n\n"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get exam TDTPOTET'}}]}]}  # check for text string
        msg = "I can't find the exam date for tdtpotet\n\n"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get default'}}]}]}  # check for text string
        msg = "Your default-time is: 1 day(s)"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get links'}}]}]}  # check for text string
        msg = "Blackboard:\nhttp://iblack.sexy\nItslearning:\nhttp://ilearn.sexy"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get link itslearning'}}]}]}  # check for text string
        msg = "Itslearning:\nhttp://ilearn.sexy"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get link blackboard'}}]}]}  # check for text string
        msg = "Blackboard:\nhttp://iblack.sexy"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'subscribe TDT4100'}}]}]}  # check for text string
        msg = None
        response = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get subscribed'}}]}]}  # check for text string
        msg = "You are subscribed to:\nTDT4100\n"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'get exams'}}]}]}  # check for text string
        msg = "The exam in TDT4100 is on 2017-05-16\n\n"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {
            'entry': [{'messaging': [{'message': {'text': 'subscribe announcement'}}]}]}  # check for text string
        msg = "You are now subscribed to announcements!"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'subscribe'}}]}]}  # check for text string
        msg = "Please specify what to subscribe to. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'subscribe TDT4100'}}]}]}  # check for text string
        msg = None
        response = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)

        test_text = {'entry': [{'messaging': [{'message': {'text': 'subscribe TDTPOTET'}}]}]}  # check for text string
        msg = None
        response = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)

        test_text = {'entry': [{'messaging': [{'message': {'text': 'unsubscribe'}}]}]}  # check for text string
        msg = "Please specify what to unsubscribe to. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {
            'entry': [{'messaging': [{'message': {'text': 'unsubscribe announcement'}}]}]}  # check for text string
        msg = "You are now unsubscribed from announcements!"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'bug'}}]}]}  # check for text string
        msg = "Please specify the bug you found. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'bug testbug'}}]}]}  # check for text string
        msg = "The bug was taken to my developers. One of them might contact you if they need further " \
              "help with the bug."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'request'}}]}]}  # check for text string
        msg = "Please specify your request. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'request testrequest'}}]}]}  # check for text string
        msg = "The request was taken to my developers. I will try to make your wish come true, but keep" \
              " in mind that not all request are feasible."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help'}}]}]}  # check for text string
        msg = "The following commands are supported:\n" \
                   "\n- Login\n- Profile\n- Get deadlines\n- Get exams\n- Get links\n- Get reminders" \
                   "\n- Get default-time\n- Get courses\n- Get commands\n- Set reminder <input>\n- Set default-time " \
                   "<input>" \
                   "\n- Delete me\n- Delete reminder <input>\n- Bug <input>\n- Request <input>\n- Subscribe <input>" \
                   "\n- Unsubscribe <input>" \
                   "\n- Help\n\nThere is also a persistent menu next to the chat area, it has shortcuts to " \
                   "some of the commands!\n\nBut that's not all, there are also some more hidden commands!\nIt " \
                   "is up to you to find them ;)\n\nIf you want a more detailed overview over a feature, you can " \
                   "visit my wiki: https://github.com/Folstad/TDT4140/wiki/Commands, or write 'help <feature>'. " \
                   "You can try this with 'help help' now!"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get subscribe'}}]}]}  # check for text string
        msg = "The 'Get subscribed' command will give you a list of all your subscribed courses." \
                           " When you are subscribed to a course, its deadlines will automatically be added to your" \
                           " reminders, and you will get the registered exam dates for it with the 'Get exams'" \
                           " command. For more info on subscriptions, type 'Help subscribe'."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get deadlines'}}]}]}  # check for text string
        msg = "Deadlines are fetched from itslearning and Blackboard with the feide username and" \
                           " password you entered with the 'login' command. To get the deadlines you can write" \
                           " the following commands:\n\t- Get deadlines\n\t- Get deadlines until <DD/MM>\n" \
                           "\t- Get deadlines from <course>\n\t- Get deadlines from <course> until <DD/MM>\n\n" \
                           "Without the <> and the course code, date and month you wish."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get exams'}}]}]}  # check for text string
        msg = "I can get the exam date for any of your courses. Just write" \
              "\n- Get exams <course_code> (<course_code2>...)."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get links'}}]}]}  # check for text string
        msg = "I can give you fast links to itslearning or Blackboard with these commands:" \
                           "\n- Get links\n- Get link itslearning\n- Get link blackboard."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get reminders'}}]}]}  # check for text string
        msg = "This gives you an overview of all upcoming reminders you have scheduled with me."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get default'}}]}]}  # check for text string
        msg = "Default-time decides how many days before an assignment's deadline you will be reminded " \
                           "by default. 'Get default-time' shows your current default-time."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help get'}}]}]}  # check for text string
        msg = "To get something type:\n- Get <what_to_get> (opt:<value1> <value2>...)\nType <help> for a " \
                       "list of what you can get"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {
            'entry': [{'messaging': [{'message': {'text': 'help get me some help'}}]}]}  # check for text string
        msg = "I'm not sure that's a supported command, if you think this is a bug, please report " \
                           "it with the 'Bug' command! If it something you simply wish to be added, use the " \
                           "'Request' command."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help set reminder'}}]}]}  # check for text string
        msg = "If you login with your feide username and password I can retrieve all your " \
                           "deadlines on itslearning and Blackboard, and remind you of them when they soon are due. " \
                            "I will naturally never share your information with " \
                           "anyone!\n\nThe following commands are supported:\n\n" \
                           "- Set reminder <Reminder text> at <Due_date>\n" \
                           "where <Due_date> can have the following formats:" \
                           "\n\n- YYYY-MM-DD HH:mm\n- DD-MM HH:mm\n- DD HH:mm\n- HH:mm\n\nand <Reminder text> is what" \
                           " I should tell you when the reminder is due. I will check " \
                           "reminders every 5 minutes."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help set default'}}]}]}  # check for text string
        msg = "I can set your default-time which decides how long before an" \
                           " assignment's deadline you will be reminded by default.\n\n" \
                           "To set your default-time please use the following format:\n\n" \
                           "- Set default-time <integer>\n\nWhere <integer> can be any number of days."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help set hueuhe'}}]}]}  # check for text string
        msg = "I'm not sure that's a supported command, if you think this is a bug, please report " \
                           "it with the 'Bug' command. If it something you simply wish to be added, use the " \
                           "'Request' command."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help set'}}]}]}  # check for text string
        msg = "To set something type:\n- Set <what_to_set> <value1> (opt:<value2>...)\nType" \
                       " <help> for a list of what you can set"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help delete reminder'}}]}]}  # check for text string
        msg = "To delete a specific reminder you first have to type <Get reminders> to find the reminder" \
                           " id, which will" \
                           "show first <index>: reminder. To delete, type:\n- Delete reminder <index> (<index2>...)\n" \
                           "\nTo delete all reminders type:\n- Delete reminders."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help delete me'}}]}]}  # check for text string
        msg = "If you want me to delete all of the information I have on you, type 'Delete me', and " \
                           "follow the instructions I give you."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help delete meexde'}}]}]}  # check for text string
        msg = "I'm not sure that's a supported command, if you think this is a bug, please report " \
                           "it with the 'Bug' command. If it something you simply wish to be added, use the " \
                           "'Request' command."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help delete'}}]}]}  # check for text string
        msg = "To delete something type:\n- Delete <what_to_delete> (opt:<value1> <value2>...)\nType " \
              "<help> for a list of what you can delete"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help help'}}]}]}  # check for text string
        msg = "The help method gives more detailed information about my features, and their commands" \
              ". You may type help in front of any method to get a more detailed overview of what it does."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help login'}}]}]}  # check for text string
        msg = "If you log in with your feide username and password I can fetch your deadlines from Blackboard " \
                   "and itslearning and give you reminders for them, but it's not necessary to log in to get " \
                   "reminders.\nIf you submitted the wrong username or password, don't worry! I will still" \
                   " remember any reminders or courses you have saved with me if you login with a new " \
                   "username and password. Be warned, though: the login page can't know whether or not you submitted " \
                   "the right username and password, it will only save what you submitted in the database."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help bug'}}]}]}  # check for text string
        msg = "If you encounter a bug please let me know! You submit a bug report with a" \
              "\n- Bug <message> \n" \
              "command. If it is a feature you wish added, please use the request command instead. " \
              "\nA bug is anything from an unexpected output to no output at all. Please include as" \
              "much information as possible about how you encountered the bug, so I can recreate it"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help request'}}]}]}  # check for text string
        msg = "If you have a request for a new feature please let me know! You submit a feature" \
              " request with a\n- Request <message> \ncommand. If you think this is already a " \
              "feature, and you encountered a bug, please use the bug command instead."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help subscribe'}}]}]}  # check for text string
        msg = "You can subscribe to courses you want to get reminders of deadlines from. When you are " \
                   "subscribed to a course, you can also get its exam date with the 'Get exams' command. " \
                   "To subscribe to a course " \
                   "just write\n- Subscribe <course_code> (<course_code2>...)."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help unsubscribe'}}]}]}  # check for text string
        msg = "You can unsubscribe from courses you don't want to get reminders of deadlines from." \
                   " When unsubscribed from a " \
                   "course, you won't get its exam dates with the 'Get exams' command. To unsubscribe from a course " \
                   "just write\n- Unsubscribe <course_code> (<course_code2>...)."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help reminders'}}]}]}  # check for text string
        msg = "There is no 'reminder' command, but type 'Set reminder' to add a new reminder, or 'Get" \
              " reminders' to see all currently active reminders. If you want more info on the format" \
              " of 'Set reminder', type 'Help set reminder'."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'help deadlines'}}]}]}  # check for text string
        msg = "Type 'Get deadlines' to get a full overview of all of your deadlines on itslearning and" \
              " Blackboard! You need to log in to use this command."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set'}}]}]}  # check for text string
        msg = "Please specify what to set. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set reminder'}}]}]}  # check for text string
        msg = 'Please specify what to be reminded of\nType help set reminder if you need help.'
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'set reminder testreminder at 23:59'}}]}]}  # check for text string
        msg = "The reminder testreminder was sat at " + \
                           datetime.now().strftime("%Y-%m-%d") + " 23:59. Reminders will be checked every 5 minutes."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, "text")

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'set reminder testreminder a 23:59'}}]}]}  # check for text string
        msg = "Please write in a supported format. Se 'help set reminder' for help. Remember to separate your text and the time of the reminder with 'at'"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'set reminder testreminder at 23:59:59'}}]}]}  # check for text string
        msg = "Please write in a supported format. Se 'help set reminder' for help."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'set reminder testreminder at 00:00'}}]}]}  # check for text string
        msg = "The reminder testreminder was sat at " + \
              (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00. Reminders will be checked every 5 minutes."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, "text")

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set class'}}]}]}  # check for text string
        msg = "Please specify what to subscribe to. Type 'Help' or visit " \
              "https://github.com/Folstad/TDT4140/wiki/Commands for a list of supported commands"
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set default-time'}}]}]}  # check for text string
        msg = 'Please specify default-time to set.'
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set default-time x'}}]}]}  # check for text string
        msg = 'Please type in an integer as default-time.'
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [{'messaging': [{'message': {'text': 'set default-time 2'}}]}]}  # check for text string
        msg = "Your default-time was set to: 2 day(s).\nTo update your deadlines " \
                                                                            "to fit this new default-time, write " \
                                                                            "'Get deadlines' or select the " \
                                                                            "'Get deadlines' option" \
                                                                            " from the menu next to the chat area."
        response, response_type = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)
        self.assertEqual(response_type, 'text')

        test_text = {'entry': [
            {'messaging': [{'message': {'text': 'skadksadk sakdksdasjdnfefjefjnfe'}}]}]}  # check for text string
        msg = None
        response = replier.arbitrate(test_id, test_text)
        self.assertEqual(response, msg)


if __name__ == '__main__':
    unittest.main()
