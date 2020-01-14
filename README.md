# Amazon Price Tracker

Keep track of multiple amazon products. As long as your computer runs this app every day, you could see how much each product's price increases or decreases over time.

## Installation

You will need python 3+ and pip.

### Google's Credentials
Watch the following video (Up to 3:51) to get your credentials and connect to a Spreadsheet. https://www.youtube.com/watch?v=cnPlKLEGR7E&t=409s

Be sure to put your 'creds.json' in the same folder as 'app.py'. It's important to make sure that the name of the credentials folder is exactly 'creds.json'.

### Install
In your terminal, Install:
```bash
pip install gspread oauth2client schedule bs4
```
gspread and oauth2client are from google and are required if you want to access google sheets.

schedule will update your google spreadsheet at midnight everyday (assuming you have this app running 24 hours 7 days a week).
If you don't plan on running the app 24/7, then dont install schedule, remove the line on the bottom of app.py that uses schedule along with the forever loop, and then add RunApp() at the very bottom. This will update your google spreadsheet every time you run the app.

### Config
Create a file named 'eVars.py' in the same folder that app.py is in.

inside of 'eVars.py', type in:
```python
SPREADSHEET_NAME =  "AmazonPriceTracker"
```
If your spreadsheet has a different name, you can change "AmazonPriceChecker" but make sure the variable name stays the same.

## Usage
On your spreadsheet, create 2 pages. The first page will contain the list of items you want to track. The second page will contain your data.

Here is an example of my sheet one:

![spreadsheet](https://user-images.githubusercontent.com/47621785/63652077-2889c600-c711-11e9-88da-13c62039d77d.png)

In case you were wondering, "owner" is used in case you would like to track an amazon product for someone else. You can put their name as "owner" to tell them apart from the products you are tracking.

Another thing, my app looks for SPECIFIC boxes so make sure that "Owner" is column A, "Link" is column B and so on. Also, you can make the list of items as long as you would like AS LONG as you start the list from row 3 as I did.

Remember not to reorder the list.

Here is an example of my sheet two:

![spreadsheet2](https://user-images.githubusercontent.com/47621785/63652126-afd73980-c711-11e9-9fd5-045b83d8cf8e.png)

DON'T type anything on your sheet 2. My app will do everything but if you want to decorate your sheet in a way where a certain row will be bold or change a certain color like I did, then you can do that yourself after running the app for the first time.
