import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from datetime import datetime

browser = webdriver.Chrome()
browser.minimize_window()

#Spreadsheet config
SPREADSHEET_NAME = "AmazonPriceChecker"
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

class item:
    def __init__(self, link, owner):
        self.link = link
        self.name = ""
        self.price = 0
        self.owner = owner
        self.num = 0 #this determins where on the spreadsheet the data will go
        self.needsToPrintInitialValues = True

def GetDate():
    currentTime = datetime.now()

    month = f"{currentTime.month:02d}"
    day = f"{currentTime.day:02d}"
    year = str(currentTime.year)[-2:]

    return str(month + "/" + day + "/" + year)

def getInfo(_item):
    #takes in a list of objects

    numOfItems = len(_item)

    for i in range(numOfItems):
        _item[i].num = i

        browser.get(_item[i].link)
        
        try:
            _item[i].price = browser.find_element_by_id("priceblock_ourprice").text
        except:
            _item[i].price = browser.find_element_by_id("priceblock_dealprice").text

        _item[i].name = browser.find_element_by_id("productTitle").text
        if(i == (numOfItems - 1)):
            print("Close browser. i = " + str(i) + " and num of items = " + str(numOfItems))
            browser.close()
        
def updateSpreadSheet(_items):
    for i in range(len(_items)):
        startingColumn = (6 * _items[i].num) + 1

        #check to see if the name, link and owner are already on row 3(first)
        for j in range(5):
            if(sheet.cell(3, startingColumn + j).value != ""):
                _items[i].needsToPrintInitialValues = False
        
        if(_items[i].needsToPrintInitialValues == True):
            #name, link, and owner have not been written.
            sheet.update_cell(2, startingColumn + 0, "Owner")
            sheet.update_cell(2, startingColumn + 1, "Product Name")
            sheet.update_cell(2, startingColumn + 2, "Product Link")
            sheet.update_cell(2, startingColumn + 3, "Date")        
            sheet.update_cell(2, startingColumn + 4, "Product Price")


            sheet.update_cell(3, startingColumn + 0, _items[i].owner)
            sheet.update_cell(3, startingColumn + 1, _items[i].name[:50])
            sheet.update_cell(3, startingColumn + 2, _items[i].link)
            sheet.update_cell(3, startingColumn + 3, GetDate())        
            sheet.update_cell(3, startingColumn + 4, _items[i].price) 
            
            
        else:
            #look for next open row
            for rowCheck in range(10000):
                #rowCheck + 4 because I want it to start looking on row 4; rowCheck will start at 0
                if(sheet.cell((rowCheck + 4), startingColumn).value == ""):
                    firstOpenRow = rowCheck + 4
                    sheet.update_cell(firstOpenRow, startingColumn + 3, GetDate())
                    sheet.update_cell(firstOpenRow, startingColumn + 4, _items[i].price)
                    break

            

            
            
            
            
        
            
        
        #find the next open row
        
        #write in the next open row only what should be repeated

        

surfacePro6 = item("https://www.amazon.com/gp/product/B07KWNFC64?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=FT3AKVF30EJ4XZYZBHJW", "manny")
gamingLaptop = item("https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=sspa_dk_detail_6?ie=UTF8&adId=A0863551GR69NSZW1EPG&qualifier=1565551617&id=485013166934304&widgetName=sp_detail2&url=%2Fdp%2FB07T9KMB91%2Fref%3Dsspa_dk_detail_6%3Fpsc%3D1", "Adriana")
ipadPro = item("https://www.amazon.com/Apple-10-5-inch-Wi-Fi-Cellular-512GB/dp/B0756651KN?ref_=Oct_TopRatedC_1232597011_0&pf_rd_r=WE348994WA2CQ1M0NXWE&pf_rd_p=f95c3cb9-0b52-52f9-b410-6f99e416af5a&pf_rd_s=merchandised-search-10&pf_rd_t=101&pf_rd_i=1232597011&pf_rd_m=ATVPDKIKX0DER", "manny")
pen = item("https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=sspa_dk_detail_1?ie=UTF8&adId=A00650512D7DORHT8DVS4&qualifier=1565551626&id=3061029219346475&widgetName=sp_detail&url=%2Fdp%2FB07C2TFPR2%2Fref%3Dsspa_dk_detail_1%3Fpsc%3D1%26pd_rd_i%3DB07C2TFPR2%26pd_rd_w%3DHVX2Y%26pf_rd_p%3D8a8f3917-7900-4ce8-ad90-adf0d53c0985%26pd_rd_wg%3DvzYee%26pf_rd_r%3DJE3YHK59DJHXA1FXQV8G%26pd_rd_r%3De3c2ba66-eb95-45da-846e-b100e7b0b04a", "manny")

items = [surfacePro6, gamingLaptop, ipadPro, pen]

getInfo(items)
updateSpreadSheet(items)


