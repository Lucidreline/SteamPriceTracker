import eVars, gspread, keyboard, requests
from   oauth2client.service_account import ServiceAccountCredentials
from   selenium import webdriver
from   datetime import datetime
from   time     import sleep

#bool variable; if true, it will send you text notifications
phoneNotification = eVars.NOTIFY

if(phoneNotification):
    #I import this here so if someone doesnt want text notifications, they dont
    #have to download twilio on pip
    from twilio.rest import Client
    account_sid = eVars.ACCOUNT_SID
    auth_token = eVars.AUTH_TOKEN

    twilioClient = Client(account_sid, auth_token)


#this opens up a chrome window
browser = webdriver.Chrome()

#this minimizes the window so that I dont have to see the amazon page
#as my computer does this in the background
keyboard.send('windows+down')
browser.minimize_window()

keyboard.send('windows+down')

# - - -Spreadsheet config - - -
#the name of the google spreadsheet
SPREADSHEET_NAME = eVars.SPREADSHEET_NAME
#honestly no clue what this does, I just know it is needed
scope  = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#goes thru my credentials. I got this from the google API credentials
creds  = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
# Lets me choose if I want to write/read different sheets.
sheet1 = client.open(SPREADSHEET_NAME).get_worksheet(0)
sheet2 = client.open(SPREADSHEET_NAME).get_worksheet(1)

#creates an empty list where all the item objects will be stored
itemsList = []

class Item:
    def __init__(self, owner, link):
        self.link  = link  #link to the amazon page where the price and name are found
        self.name  = ""    #This is assigned when the amazon page is pulled up
        self.price = 0     #This is assigned when the amazon page is pulled up
        self.owner = owner #who is tracking the product
        self.num   = 0     #this determins where on the spreadsheet the data will go
        self.needsToPrintInitialValues = True #This is reassigned later
        self.phoneNumber = "" #Used to send a text message notification

def DollarsToFloat(dollars):
    #converts $1,899.00 into 1899.00
    #removes the dollar sign
    dollars = dollars[1:]

    #removes commas
    dollars = dollars.replace(',', '')
    return float(dollars)

def GetDate():
    #gets the current time
    currentTime = datetime.now()

    #gets the month & day and makes sure that it is 2 digits atleast; 5 -> 05
    month = f"{currentTime.month:02d}"
    day   = f"{currentTime.day:02d}"
    #gets last 2 digits of the year
    year  = str(currentTime.year)[-2:] 

    #puts date into 'mm/dd/yy' format
    return str(month + "/" + day + "/" + year)

def ReadUserList(_itemsList):
    #loop each row until an empty row is found
    for rowNum in range(10000):
        #this sleep is too stop passing the google sheets quota
        sleep(.2)
        #adds 3 because I want it to start looking on row 3
        rowNum = rowNum + 3
        
        #checks to see if the cell contains data; if its not empty
        if(sheet1.cell(rowNum, 1).value != ""):
            #pack info from spreadsheet into an object
            itemObject = Item(sheet1.cell(rowNum, 1).value, sheet1.cell(rowNum, 2).value)
            itemObject.name = sheet1.cell(rowNum, 3).value
            itemObject.phoneNumber = sheet1.cell(rowNum, 4).value
            #send object to the front of the list
            _itemsList.append(itemObject)
        else:
            break
                   
def GetProductInfo(_itemsList):
    #takes in a list of objects

    #gets the number of objects in the list of objects
    numOfItems = len(_itemsList)

    #Loops through every object in the list
    for i in range(numOfItems):
        #assigns each element a number to determine where on the spreadsheet this will be written
        _itemsList[i].num = i

        #opens the link to the amazon product
        browser.get(_itemsList[i].link)

        if(len(browser.find_elements_by_id("priceblock_ourprice")) > 0):
            _itemsList[i].price = browser.find_elements_by_id("priceblock_ourprice")[0].text
        elif(len(browser.find_elements_by_id("priceblock_dealprice")) > 0):
            _itemsList[i].price = browser.find_elements_by_id("priceblock_dealprice")[0].text
        else:
            _itemsList[i].price = "Unavailable"
            
        #finds the name of the product
        ##_itemsList[i].name = browser.find_element_by_id("productTitle").text

        #If it is the last object in the list, then it closes the browser
        if(i == (numOfItems - 1)):
            browser.close()
        
def TextNotification(__item, row, col):
    sleep(.1)
    firstPriceCheck   = str(sheet2.cell(3, col).value)
    firstPriceCheck = DollarsToFloat(firstPriceCheck)

    currentPriceCheck = str(sheet2.cell(row, col).value)
    currentPriceCheck = DollarsToFloat(currentPriceCheck)

    priceDiffPercent = (currentPriceCheck/firstPriceCheck) * 100
    priceDiffPercent = 100 - priceDiffPercent

    if(phoneNotification):
        percentLimitBeforeAlert = eVars.PERCENT_OFF

    if(priceDiffPercent >= percentLimitBeforeAlert and __item.phoneNumber != "" and phoneNotification):
        Message = __item.name + "'s price has drop atleast " + str(priceDiffPercent) + "%!"
        #formulate the message that will be sent
        message = twilioClient.messages.create(
        to=__item.phoneNumber,
        from_= eVars.TRIAL_PHONE_NUM,
        body=Message)

def UpdateSpreadSheet(_itemsList):
    #loops through every object in the objects list
    for i in range(len(_itemsList)):
        #this sleep is too stop passing the google sheets quota
        sleep(.1)
        #uses the assigned object number to determine where the first column of the data will be
        startingColumn = (6 * _itemsList[i].num) + 1

        #checks to see if the name, link and owner are already on row 3(first row)
        #5 for range because each item takes up 5 columns
        for j in range(5):
            #if all cells in the item's cells are empty
            if(sheet2.cell(3, startingColumn + j).value != ""):
                _itemsList[i].needsToPrintInitialValues = False
        
        #this prints out the initial information
        if(_itemsList[i].needsToPrintInitialValues == True):
            #starting column is determined by the item number, then I add a number to that
            #to put information in the columns next to it

            #name, link, and owner have not been written.
            sheet2.update_cell(2, startingColumn + 0, "Owner")
            sheet2.update_cell(2, startingColumn + 1, "Product Name")
            sheet2.update_cell(2, startingColumn + 2, "Product Link")
            sheet2.update_cell(2, startingColumn + 3, "Date")        
            sheet2.update_cell(2, startingColumn + 4, "Product Price")

            #Puts the first day's information
            #thi is printed a row under ^
            sheet2.update_cell(3, startingColumn + 0, _itemsList[i].owner)
            sheet2.update_cell(3, startingColumn + 1, _itemsList[i].name[:50])
            sheet2.update_cell(3, startingColumn + 2, _itemsList[i].link)
            sheet2.update_cell(3, startingColumn + 3, GetDate())        
            sheet2.update_cell(3, startingColumn + 4, _itemsList[i].price) 
                   
        else:
            #look for next open row
            for rowCheck in range(10000):
                #rowCheck + 3 because I want it to start looking on row 3; rowCheck will naturally start at 0
                if(sheet2.cell((rowCheck + 3), startingColumn + 3).value == ""):
                    firstOpenRow = rowCheck + 3
                    #prints out the date and price on the next open row same column
                    sheet2.update_cell(firstOpenRow, startingColumn + 3, GetDate())
                    sheet2.update_cell(firstOpenRow, startingColumn + 4, _itemsList[i].price)
                                 
                    #sends a text notification if the price drops 10 bucks
                    TextNotification(_itemsList[i], firstOpenRow, startingColumn + 4)
                    break
            
#Run the 3 main methods and pass in the list of item objects
ReadUserList(itemsList)
GetProductInfo(itemsList)
UpdateSpreadSheet(itemsList)

quit()