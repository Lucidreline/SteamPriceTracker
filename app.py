from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from datetime import datetime
from urllib import request
from time import sleep
import eVars, gspread
import schedule

# - - -Spreadsheet config - - -
SPREADSHEET_NAME = eVars.SPREADSHEET_NAME #the name of the google spreadsheet
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
        sleep(100)
        #adds 3 because I want it to start looking on row 3
        rowNum = rowNum + 3
        
        #checks to see if the cell contains data; if its not empty
        if(sheet1.cell(rowNum, 1).value != ""):
            #pack info from spreadsheet into an object
            itemObject = Item(sheet1.cell(rowNum, 1).value, sheet1.cell(rowNum, 2).value)
            itemObject.name = sheet1.cell(rowNum, 3).value
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


        sauce = request.urlopen(_itemsList[i].link).read() #opens the link to the user's amazon product
        soup = BeautifulSoup(sauce, "lxml") #parses it so that we can extract what we need (the prices)

        if(soup.find(id="priceblock_ourprice")): #checks to make sure this id exsists
            _itemsList[i].price = soup.find(id="priceblock_ourprice").text.strip() #if it does, this will be our price
        elif(soup.find(id="priceblock_dealprice")):
            _itemsList[i].price = soup.find(id="priceblock_dealprice").text.strip()
        elif(soup.find(id="priceblock_saleprice")):
            _itemsList[i].price = soup.find(id="priceblock_saleprice").text.strip()
        else:
            _itemsList[i].price = "Unavailable" #if we were not able to find a price
            print("We were unable to find the price for: " + _itemsList[i].link) #prints an error for me to see if the logs

def UpdateSpreadSheet(_itemsList):
    for i in range(len(_itemsList)): #loops through every object in the objects list
        sleep(100) #this sleep is too stop passing the google sheets quota
        startingColumn = (6 * _itemsList[i].num) + 1 #uses the assigned object number to determine where the first column of the data will be

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
                                 
                    break

def sayHi():
    nowSON = datetime.now()
    current_time = nowSON.strftime("%H:%M:%S")
    print("hi from ", current_time)

def RunApp():
    #Run the 3 main methods and pass in the list of item objects
    rightNow = datetime.now()
    current_time = rightNow.strftime("%H:%M:%S")
    current_date = rightNow.strftime("%Y-%m-%d %H:%M:%S")
    print("\n\nStarting App\nTime:", current_time, "\nDate:", current_date)

    try:
        ReadUserList(itemsList)
        GetProductInfo(itemsList)
        UpdateSpreadSheet(itemsList)

        current_time = rightNow.strftime("%H:%M:%S")
        current_date = rightNow.strftime("%Y-%m-%d %H:%M:%S")
        print("\n\nDaily Check-up\nTime:", current_time, "\nDate:", current_date, "\nNo Current errors")

    except:
        current_time = rightNow.strftime("%H:%M:%S")
        current_date = rightNow.strftime("%Y-%m-%d %H:%M:%S")
        print("\n\nDaily Check-up\nTime:", current_time, "\nDate:", current_date, "\nRan into an error")

 
rightNow = datetime.now()
current_time = rightNow.strftime("%H:%M:%S")
current_date = rightNow.strftime("%Y-%m-%d %H:%M:%S")
print("\n\nStarting App\nTime:", current_time, "\nDate:", current_date)

schedule.every().day.at("00:00").do(RunApp)  #app will be run every day at midnight
while True:
    schedule.run_pending()