import requests,json,colorama,time,os
from pushbullet import Pushbullet
from bs4 import BeautifulSoup as soup
from colorama import Fore, Style
from datetime import datetime
from os import system
from time import sleep
colorama.init()

system(f'mode con: cols=30 lines=20')
system("title " + "SkinPort Bot")


while True:
    with open('config.json') as f:
        config = json.load(f)
    try:
        API_Key = config.get('API')
        pb = Pushbullet(API_Key)
    except:
        pass
    link = config.get('Link')
    Itemname = config.get('Name')
    Itemprice = config.get('Price')
    time = config.get('Time')
    page = requests.get(link)
    soupP = soup(page.content,'lxml')
    items = soupP.find_all("div", class_="ItemList-item")
    for item in items:
        name = item.find("div", class_="ItemPreview-itemName")
        price = item.find("div", class_="Tooltip-link")
        if name.text == Itemname:
            floatprice = price.text.replace("€","")
            if float(floatprice) <= float(Itemprice):
                print(Fore.LIGHTGREEN_EX+f"{name.text}"+Fore.LIGHTWHITE_EX+f"[{price.text}]")
                try:
                    push = pb.push_note(f"New {name.text} Available",f"There is currently a {name.text} for {price.text}")
                except:
                    pass
            else:
                print(Fore.LIGHTRED_EX+f"{name.text}"+Fore.LIGHTWHITE_EX+f"[{price.text}]")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("")
    print(Fore.LIGHTWHITE_EX+"LastChecked:"+Fore.LIGHTYELLOW_EX+current_time)
    sleep(int(time))
    os.system("cls")
