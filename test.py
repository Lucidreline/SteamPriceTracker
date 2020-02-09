from bs4 import BeautifulSoup
import requests


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
cookies = {'birthtime': '568022401', 'mature_content': '1' }
page = requests.get("https://store.steampowered.com/app/374320/DARK_SOULS_III/", headers=headers, cookies=cookies) #opens the link to the user's amazon product
soup = BeautifulSoup(page.content, "lxml") #parses it so that we can extract what we need (the prices)


if soup.find("div", class_="discount_final_price"):
    print(soup.find("div", class_="discount_final_price").text.strip())
elif soup.find("div", class_="game_purchase_price price"):
    print(soup.find("div", class_="game_purchase_price price").text.strip())

print("hi")
