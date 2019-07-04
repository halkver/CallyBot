from flask import Flask, request
import reply
import help_methods
import thread_settings
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import credentials
import callybot_database
from datetime import datetime
from MySQLdb import OperationalError
import restart_VPN
import logg
import sys

sys.stdout = logg.Logger(sys.stdout, open('log.txt', 'a'))  # Writes to file and console
app = Flask(__name__)
credential = credentials.Credentials()
db_credentials = credential.db_info
db = callybot_database.CallybotDB(db_credentials[0], db_credentials[1], db_credentials[2], db_credentials[3])
replier = reply.Reply(credential.access_token, db)
received_message = []


def init():
    reminder_interrupt()
    restart_vpn_interrupt()
    clear_old_reminders()
    thread_handler = thread_settings.ThreadSettings(credential.access_token)
    thread_handler.whitelist("https://folk.ntnu.no/halvorkmTDT4140/")
    thread_handler.set_greeting(
        "Hi there {{user_first_name}}!\nWelcome to CallyBot. Press 'Get Started' to get started!")
    thread_handler.set_get_started()
    return thread_handler.set_persistent_menu()


def clear_old_reminders():
    """Clears old reminders, which were not checked while database was down"""
    reminders = db.get_all_reminders()
    for reminder in reminders:
        if reminder[0] < datetime.now():
            print("Deleting old reminder: ", reminder)
            db.delete_reminder(reminder[4])


def restart_vpn_interrupt():
    vpn_scheduler = BackgroundScheduler()
    vpn_scheduler.start()
    vpn_scheduler.add_job(
        func=restart_vpn,
        trigger=CronTrigger(hour="5", minute="2"),  # running every day at 5:02
        id='restart_vpn',
        name='VPN_restart',
        replace_existing=True)
    atexit.register(lambda: vpn_scheduler.shutdown())


def restart_vpn():
    print("Restarting VPN...")
    restart_VPN.restart_vpn()
    print("VPN restarted")


def reminder_interrupt():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=reminder_check,
        trigger=CronTrigger(minute='0,5,10,15,20,25,30,35,40,45,50,55'),  # checking every 5th minute
        id='reminder_check',
        name='Reminder',
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())


def reminder_check():
    # Run reminder_check
    try:
        current = help_methods.search_reminders(db)
    except OperationalError:  # MySQL not available at this time, tries again in 1 minute
        time.sleep(60)
        current = help_methods.search_reminders(db)
    print("Reminder trigger" + str(time.ctime()) + ". Reminders found:", current)
    if current:
        for reminder in current:
            replier.reply(reminder[1], "Reminder: " + reminder[2], "text")
    return current


@app.route('/', methods=['POST'])  # pragma: no cover
def handle_incoming_messages():  # pragma: no cover
    """Handles incoming POST messages, has 'pragma: no cover' due to pytest throwing an error
    when handling flask application methods, and internal testing is not needed as this is 
    properly tested trough blackbox"""
    data = request.json
    print("\n\n")
    print("----------------START--------------")
    print("DATA:", end="")
    try:
        user_id = data['entry'][0]['messaging'][0]['sender']['id']
        print(data)
        print("---------------END-----------------\n")
    except KeyError:  # No sender id
        return "ok", 200
    global received_message
    try:
        if "postback" not in data['entry'][0]['messaging'][0]:  # Is not menu reply
            message_id = data['entry'][0]['messaging'][0]['message']['mid']
            if message_id in received_message:
                print("Duplicated message", data, "\nCurrent message list:", received_message)
                return 'ok', 200
            else:
                if len(received_message) > 255:
                    received_message = received_message[-32:]
                received_message.append(message_id)
        else:
            message_id = ""
    except (KeyError, TypeError):
        print("Error: Could not find message_id, or unknown format")
        return "ok", 200
    try:
        replier.arbitrate(user_id, data)
    except OperationalError:
        if message_id in received_message:
            received_message.remove(message_id)
        return "Internal Server Error", 500
    print("ok 200 for message to " + user_id)
    return "ok", 200


@app.route('/', methods=['GET'])  # pragma: no cover
def handle_verification():  # pragma: no cover
    """Handles incoming GET messages, has 'pragma: no cover' due to pytest throwing an error
    when handling flask application methods. This method is properly tested by connectig the server
    to the server"""
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args['hub.verify_token'] == credential.verify_token:
            return request.args['hub.challenge'], 200
        else:
            return "Invalid verification token", 403
    return 'ok', 200


if __name__ == '__main__':
    init()
    app.run(threaded=True)
