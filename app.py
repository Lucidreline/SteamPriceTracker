from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import eVars, gspread
import requests

# - - - Spreadsheet config - - -
SPREADSHEET_NAME = eVars.SPREADSHEET_NAME #the name of the google spreadsheet

#honestly no clue what this does, I just know it is needed
scope  = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

#goes thru my credentials. I got this from the google API credentials
creds  = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Lets me choose if I want to read/write different sheets.
sheet1 = client.open(SPREADSHEET_NAME).get_worksheet(0)
sheet2 = client.open(SPREADSHEET_NAME).get_worksheet(1)


itemsList = [] #creates an empty list where all the item objects will be stored

class Item:
    def __init__(self, owner, link):
        self.link  = link  #link to the Steam page where the price and name are found
        self.name  = ""    #This is assigned when the Steam page is pulled up
        self.price = 0     #This is assigned when the Steam page is pulled up
        self.owner = owner #who is tracking the Game
        self.num   = 0     #this determins where on the spreadsheet the data will go
        self.needsToPrintInitialValues = True #This is reassigned later
    def __str__(self):
        return "\nname: " + self.name + "\nlink: " + self.link + "\nnum: " + str(self.num)

# - - - The App's main functions - - -
def DollarsToFloat(dollars):
    dollars = dollars[1:] #converts $1,899.00 into 1899.00 and removes the dollar sign
    dollars = dollars.replace(',', '') #removes commas
    return float(dollars)

def GetDate():
    currentTime = datetime.now()

    #gets the month & day and makes sure that it is 2 digits atleast; 5 -> 05
    month = f"{currentTime.month:02d}"
    day   = f"{currentTime.day:02d}"
    year  = str(currentTime.year)[-2:] #gets last 2 digits of the year

    return str(month + "/" + day + "/" + year)

def ReadUserList(_itemsList):
    #loop each row until an empty row is found
    for rowNum in range(10000):
        #this sleep is too stop passing the google sheets quota
        sleep(10)
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
                   
def GetGameInfo(_itemsList): #takes in a list of objects
    numOfItems = len(_itemsList) #gets the number of objects in the list of objects

    for i in range(numOfItems): #Loops through every object in the list
        _itemsList[i].num = i #assigns each element a number to determine where on the spreadsheet this will be written

        # Header helps avoids the 502 error
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
        cookies = {'birthtime': '568022401', 'mature_content': '1' }
        page = requests.get(itemsList[i].link, headers=headers, cookies=cookies) #opens the link to the user's Steam game
        soup = BeautifulSoup(page.content, "lxml") #parses it so that we can extract what we need (the prices)

        
        if soup.find("div", class_="game_purchase_price price"):
            _itemsList[i].price = soup.find("div", class_="game_purchase_price price").text.strip()
        elif soup.find("div", class_="discount_final_price"):
            _itemsList[i].price = soup.find("div", class_="discount_final_price").text.strip()
        else:
            _itemsList[i].price = "Unavailable" #if we were not able to find a price
            print("We were unable to find the price for: " + _itemsList[i].link) #prints an error for me to see if the logs

        if _itemsList[i].price == 'Free To Play':
            _itemsList[i].price = '$0.00'

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
            sheet2.update_cell(2, startingColumn + 1, "Game Name")
            sheet2.update_cell(2, startingColumn + 2, "Game Link")
            sheet2.update_cell(2, startingColumn + 3, "Date")        
            sheet2.update_cell(2, startingColumn + 4, "Game Price")

            #Puts the first day's information
            #thi is printed a row under ^
            sheet2.update_cell(3, startingColumn + 0, _itemsList[i].owner)
            sheet2.update_cell(3, startingColumn + 1, _itemsList[i].name[:50])
            sheet2.update_cell(3, startingColumn + 2, _itemsList[i].link)
            sheet2.update_cell(3, startingColumn + 3, GetDate())        
            sheet2.update_cell(3, startingColumn + 4, _itemsList[i].price) 
                   
        else:
            for rowCheck in range(10000): #look for next open row
                #rowCheck + 3 because I want it to start looking on row 3; rowCheck will naturally start at 0
                if(sheet2.cell((rowCheck + 3), startingColumn + 3).value == ""):
                    firstOpenRow = rowCheck + 3
                    #prints out the date and price on the next open row same column
                    sheet2.update_cell(firstOpenRow, startingColumn + 3, GetDate())
                    sheet2.update_cell(firstOpenRow, startingColumn + 4, _itemsList[i].price)
                                 
                    break #breaks out of the long loop because we dont have to look for more rows to add this item

def TimeStamp():
    rightNow = datetime.now()
    current_time = rightNow.strftime("%H:%M:%S")
    current_date = rightNow.strftime("%m/%d/%Y")
    return "\nTime: " + current_time + "\nDate: " + current_date


# - - - Running the App - - -
def RunApp():

    #Run the 3 main methods and pass in the list of item objects
    print("\nApp has been called")

    ReadUserList(itemsList)
    print("App Has read the User's list")

    GetGameInfo(itemsList)
    print("App has collected the game prices")

    UpdateSpreadSheet(itemsList)
    print("App Has updated the spreadsheet. No Errors occurred" + "\n\nTimeFinished:" + TimeStamp(),"\n\n")
    
    
    
print("\n\nStarting App", TimeStamp())

# # - - - Scheduling the App - - -
while True:
    currentTime = datetime.now()
    currentHour = currentTime.hour
    currentMinute = currentTime.minute
    currentSecond = currentTime.second

    #Chekcs if it is midnight, It will still work 2 seconds after just incase the app sleeps at exactly midnight, it will still have a second window to run
    if currentHour == 0 and currentMinute == 0 and (currentSecond >= 0 and currentSecond < 2): 
        RunApp()
    sleep(2) #keeps the cpu usage percentages down on my server, I like to exaggerate