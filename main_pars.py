import requests
from bs4 import BeautifulSoup
from time import sleep

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
MAINLINK = "https://scrapingclub.com"

def download_card(url):
    resp = requests.get(url, stream=True)
    r = open("images\\" + url.split('/')[-1], "wb")
    for value in resp.iter_content(1048576):
        r.write(value)
    r.close()

def get_url():
    for count in range(1, 7):
        link = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        responce = requests.get(link, headers=header).text
        soup = BeautifulSoup(responce, 'lxml')

        data = soup.find_all('div', class_="w-full rounded border")

        for i in data:
            card_url = MAINLINK + i.find("a").get("href")
        yield card_url

def pars_card():
    for card_url in get_url():
        responce = requests.get(card_url, headers=header).text
        sleep(3)
        soup = BeautifulSoup(responce, 'lxml')
        data = soup.find('div', class_="my-8 w-full rounded border")

        name = data.find("h3", class_="card-title").text
        price = data.find("h4", class_="my-4 card-price").text
        description = data.find("p", class_="card-description").text
        img_link = MAINLINK + data.find("img").get("src")
        download_card(img_link)
        yield name, price, description, img_link