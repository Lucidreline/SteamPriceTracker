import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver

browser = webdriver.Chrome()

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
        
def updateSpreadSheet(_items):
    for i in range(len(_items)):
        startingColumn = (5 * _items[i].num) + 2

        sheet.update_cell(3, startingColumn + 0, _items[i].price)
        sheet.update_cell(3, startingColumn + 1, _items[i].name)
        sheet.update_cell(3, startingColumn + 2, _items[i].link)
        sheet.update_cell(3, startingColumn + 3, _items[i].owner)

surfacePro6 = item("https://www.amazon.com/gp/product/B07KWNFC64?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=FT3AKVF30EJ4XZYZBHJW", "manny")
gamingLaptop = item("https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=sspa_dk_detail_6?ie=UTF8&adId=A0863551GR69NSZW1EPG&qualifier=1565551617&id=485013166934304&widgetName=sp_detail2&url=%2Fdp%2FB07T9KMB91%2Fref%3Dsspa_dk_detail_6%3Fpsc%3D1", "Adriana")
ipadPro = item("https://www.amazon.com/Apple-10-5-inch-Wi-Fi-Cellular-512GB/dp/B0756651KN?ref_=Oct_TopRatedC_1232597011_0&pf_rd_r=WE348994WA2CQ1M0NXWE&pf_rd_p=f95c3cb9-0b52-52f9-b410-6f99e416af5a&pf_rd_s=merchandised-search-10&pf_rd_t=101&pf_rd_i=1232597011&pf_rd_m=ATVPDKIKX0DER", "manny")

items = [surfacePro6, gamingLaptop, ipadPro]

getInfo(items)
updateSpreadSheet(items)
