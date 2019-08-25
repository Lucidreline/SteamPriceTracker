# Amazon Price Tracker

Keep track of multiple amazon products. As long as your computer runs this app every day, you could see how much each product's price increases or decreases over time.

## Installation

You will need windows, chrome, pip, and python 3+.

### Google's Credentials
Watch the following video (Up to 3:51) to get your credentials and connect to a Spreadsheet. https://www.youtube.com/watch?v=cnPlKLEGR7E&t=409s

Be sure to put your 'creds.json' in the same folder as 'app.py'. It's important to make sure that the name of the credentials folder is exactly 'creds.json'.

### Install
In your terminal, Install:
```bash
pip install gspread oauth2client selenium keyboard twilio
```
gspread and oauth2client are from google and are required if you want to access google sheets

selenium is used to go to amazon.com and extract the prices

keyboard is used to do a shortcut which minimized the browser window

twilio is optional, it allows you to get notifications (Read more about this further down).

### ChromeDriver
Open your chrome browser and click the 3 little dots on the top right. Hover over 'Help' and select 'About Google Chrome'. Here you will see a version number. 

visit https://chromedriver.chromium.org/downloads and download the chromedriver for your chrome browser version.

After downloading the 'chromedriver.exe', place it in a permanent location on your computer. You don't want to move it around. Copy the path to the folder that contains your chrome driver.

For example, if your chromedriver is in your documents, the path would be C:\Users\ma52c\Documents. Instead of 'ma52c' you would put in your username.

After you have your path, push your windows key and search for 'env' and select 'Edit the system environment variables'. Click the 'Environment Variables...' button. Near the top under 'User variables for <Your Username>' you should see a variable named 'Path'. Select that variable and click 'Edit'.

You should now see a list of paths. Click 'New' and paste in the path to the 'chromedriver.exe' from earlier.

Then, hit "Ok", then "Ok" again, and you guessed it, "Ok" again.

To make sure this worked, Open your terminal and type in:
```bash
chromedriver
```

if you "Starting ChromeDriver blah blah blah..." Then you're golden!

### Config
Create a file named 'eVars.py' in the same folder that app.py is in.

inside of 'eVars.py', type in:
```python
SPREADSHEET_NAME =  "AmazonPriceChecker"
```
If your spreadsheet has a different name, you can change "AmazonPriceChecker" but make sure the variable name stays the same.

### Notifications
If you are not interested in text notifications, type the following in 'eVars.py' and then skip to the Usage section
```python
NOTIFY = False
```

If you WOULD like to receive text notifications when your product dropped a certain amount in price, type the following in 'eVars.py':
```python
NOTIFY = True
PERCENT_OFF = 15
```
PERCENT_OFF will set when to send you a notification. In this case, you will get a notification when your product is 15% off or more.

Next, visit https://www.twilio.com and sign up for a free trial account. In the sign in process, they will give you a phone number.

After, go to your dashboard and find your ACCOUNT SID and AUTH TOKEN (You will need to click on 'show' to see your AUTH TOKEN). 

go back to 'eVars.py' and put in your ACCOUNT SID, AUTH TOKEN, and the phone number that they gave you:
```python
ACCOUNT_SID = 'abCdEFGhIjklO1234'
AUTH_TOKEN = '123456supersecure'
TRIAL_PHONE_NUM = '+15547435921'
```
Be sure to spell and capitalize the variable names exactly as I did.

## Usage
On your spreadsheet, create 2 pages. The first page will contain the list of items you want to track. The second page will contain your data.

Here is an example of my sheet one:

![spreadsheet](https://user-images.githubusercontent.com/47621785/63652077-2889c600-c711-11e9-88da-13c62039d77d.png)

In case you were wondering, "owner" is used in case you would like to track an amazon product for someone else. You can put their name as "owner" to tell them apart from the products you are tracking. You can even add their phone number as long as you verify their number on twilio.

You can verify a number on Twilio by going to your dashboard (where you found the Account SID and Token) and clicking the Verified Numbers link:

![VerifiedNumbers](https://user-images.githubusercontent.com/47621785/63652133-bf568280-c711-11e9-96b2-b54e1b4ca304.png)

My app looks for SPECIFIC boxes so make sure that "Owner" is column A, "Link" is column B and so on. Also, you can make the list of items as long as you would like AS LONG as you start the list from row 3 as I did.

Remember not to reorder the list.

Here is an example of my sheet two:

![spreadsheet2](https://user-images.githubusercontent.com/47621785/63652126-afd73980-c711-11e9-9fd5-045b83d8cf8e.png)

You don't have to type ANYTHING on your sheet 2. My app will do everything but if you want to make a certain row bold or a certain color like I did, then you can do that yourself after running the app for the first time.









