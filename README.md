
# CallyBot
NTNU Software Development Project - Team 57 Pentum </br></br>
CallyBot is a software project under development. Cally helps you with reminders, assignment deadlines and exam dates. More functions may be added in the future. Assignment deadlines are currently only supported for students using itslearning and Blackboard through Feide at NTNU. The only courses currently available are NTNU courses, which means that the only exam dates you can get are from these courses. </br></br>
## Join and talk to CallyBot today
To talk with Cally click [here](http://m.me/CallyBot). The bot CallyBot will not answer until it is released public, or you are added as a test user. To be added as a test user, send her a message [here](http://m.me/CallyBot) and you will be added as soon as possible.

### Features
The supported commands for the CallyBot are listed under [the wiki.](https://github.com/Folstad/TDT4140/wiki/Commands)

## Instructions - How to set up CallyBot from scratch 
### 1. Create a Facebook page
First you have to [create](https://www.facebook.com/pages/create/) a Facebook page from which the bot will communicate through.<br /> 
Then choose what kind of page you want, it does not really matter. The only important thing is to make it through your own Facebook profile.
### 2. Create an app at Facebook developer
Go to [Facebook developer](https://developers.facebook.com/) and login. Go to **My apps** and select **Add a new app**.<br />
Write in a name for your app and choose category as **Apps for Messenger**.<br />
Next, go to the section **App Review for Messenger**, add **pages_messaging** and **pages_messaging_subscriptions** to submission.<br />
Before we check out the code find the section **Token Generator**, select your page and save the **Page Access Token** you get. We will use that later when we connect the bot and app together.
### 3. Setup the server
Now it is time to look at the code. First you have to pull all the files from the **master** branch. Be sure to install all the required libraries if you do not already have installed them. Currently we are using these libraries:
* mysqlclient - MySQLdb for python3, for connecting to mysql database.
* Flask - To handle post/get requests from Facebook.
* requests - To handle incoming data from Flask, and to send data.
* selenium - To webscrape and general interaction with websites<sup>1</sup>.
* pycrypto - To decrypt passwords from database<sup>2</sup>.
* apscheduler - To handle interrupts to check database for reminders.

To install all packages, locate requirements.txt on your computed, open your terminal there, and run
```
pip install -r requirements.txt
```

A **credentials.py** file will also be needed, it should have the following format:
```
class Credentials:  # Add credentials here
    def __init__(self):
        self.access_token = Your_access_token        
        self.verify_token = Your_verify_token
        self.db_info = (URL_to_database, Login_name, Login_password, Database_name)
        self.key = Your_encryption_key
        self.feide = (A_feide_login_name, The_encrypted_password)  # This is only used in testing

```
Begin by adding the access token you generated earlier in the correct field. Enter a verify token and a key, the verify token is used when connection the bot to facebook, chose a safe password. The key is used in encryption, it should consist of 32 characters. The database information should be inserted into its field. The database structure supported by this code follows ![this ER scheme](http://i.imgur.com/GX2U4RJ.png)<br />
Now when you run the **server_main.py** file the server will run locally. We want to put it online. To do so we use [ngrok](https://ngrok.com/download)<br />
To use it, run the exe file with arguments **http** and **used_port**. We have not specified any port in the code, so Flask will use the default which is 5000. For instance:
```
./ngrok http 5000
```
or
```
ngrok http 5000
```
Be sure to be in the folder in which ngrok was downloaded <br /><br />
If everything went as it should ngrok has now given you a https url which points to your local port.<br />
Copy this url then run the **server_main.py** file. The current code uses an MySQL. We spessificly use servers from NTNU, which requires the code to be launched from within NTNU's eduroam, or on a computer running the [NTNU VPN](https://innsida.ntnu.no/wiki/-/wiki/English/Install+VPN?_36_pageResourcePrimKey=915712). <br />
Now go back to the app creation page and click on **+ Add Product**. Choose **webhook** and click **New subscription** and select **Page**<br /><br />
Be sure to be in the folder in which ngrok was saved. <br /><br />
If everything went as it should, ngrok has now given you a https url which points to your local port.<br />
Copy this url and then run the **server_main.py** file.<br />
Now go back to the app creation page and click on **+ Add Product**. Choose **webhook**, click **New subscription** and select **Page**.<br /><br />
In the **Callback URL** field, paste the url you got from ngrok. In the **Verify Token** field type in the token you chose in your **credentials** file. <br /><br />
In the **Subscription Fields**, choose **messages** and **messaging_postbacks**. <br />
Now press **Verify and save**. Now you should see a **POST** request in ngrok and server_main with **200 ok** or similar as answer. If you do not, go over the steps and see if you missed anything. <br /><br />
To complete the setup, go back to **Messenger** under **Products** and go to the **Webhooks** section. Select your page and make it subscribe to the webook. <br /><br />
Now you should be good to go! Have fun chatting! <br/><br />
#### Notes
Every time you start ngrok you get a new url. Be sure to change the webhook url to this. Also, if you shut down ngrok (the url) for too long, the webhook will be disabled. To fix this, you need to first update it with the new url, then make the page resubscribe to the webhook. <br /><br />

## Testing
To test that the code runs correctly, you should run the included test\_ files. You will need to insert supported values into the feide field in the **credentials.py** file discussed earlier. This code is made to support pytest, to run all tests, and see a detailed overview of the test coverage, install the pytest library or run
```
pip install -r test_requirements.txt
```
With the terminal open at the codes location, simply write
```
./pytest
```
or
```
pytest
```
to run the test with predefined configuration as spessified in setup.cfg and .coveragerc.


## Coding Description
In this project, the chosen coding convention is PEP 8 for the Python Code. Further detailed information can be found [here](https://www.python.org/dev/peps/pep-0008/#introduction). The Python code is written in Python 3.5. <br /><br />
The files does the following tasks:
*	**callybot_database.py** - Handles all communication with the database.
*	**dummy_main.py** - Manual testing file. Initializes a local dummy server. This server neither connects to Facebook nor initializes interrupts. Text can be written into the console as if written from a user to the local code version, and the reply is sent to the chosen user id in the file. 
*	**help_methods.py** - Various help methods.
*	**iblack_scrape.py** - Web scraping of Blackboard.
*	**ilearn_scrape.py** - Web scraping of Itslearning.
*	**logg.py** - Changes the location of all print messages in the running code. Currently called to have all print statements write both to console and log.txt.
*	**reply.py** - Handles all messages retrieved by the bot.
*	**restart_VPN.py** - Restarts the VPN to prevent timeout.
*	**scraper.py** - Schedules scraping of deadlines.
*	**server_main.py** - **Main file.** Initializes all other files with appropriate parameters and handles all requests from Facebook.
*	**thread_settings.py** - Initializes the settings for the Facebook chats used by the bot
 

## Support
Our team is here to help if you have any questions. There are several ways to get in touch with our team member:
* Get support by joining our communication channel on Facebook Messenger [here](http://m.me/CallyBot).
* Report issues [here](https://github.com/Folstad/TDT4140/issues) by opening a Github Issue on our repository.


<sup>1</sup> To use selenium you need to add [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) to __**PATH**__ or put it in your standard exe folder.<br />
<sup>2</sup> Pycrypto is not currently supported by python 3.6, but is supported by python versions up to 3.5.3. Requires [C++ 15 compiler](http://landinghub.visualstudio.com/visual-cpp-build-tools) to install. *Tested with 'Download Visual C++ Build Tools 2015'.*
