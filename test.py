from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
page = requests.get("https://store.steampowered.com/app/1076500/Valgrave_Immortal_Plains/", headers=headers) #opens the link to the user's amazon product
soup = BeautifulSoup(page.content, "lxml") #parses it so that we can extract what we need (the prices)

if soup.find("div", class_="discount_final_price"):
    print(soup.find("div", class_="discount_final_price").text.strip())
elif soup.find("div", class_="game_purchase_price price"):
    print(soup.find("div", class_="game_purchase_price price").text.strip())
