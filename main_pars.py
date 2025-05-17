import requests
from bs4 import BeautifulSoup
from time import sleep
import random

# Список десктопных users
users = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
]

# Выбор случайной строки users
user = random.choice(users)

# Указываем user agent в заголовках запроса перед выполнением запроса
header = {"user-agent": user}

# Страница сайта, которую будем парсить
MAINLINK = "https://scrapingclub.com"

# Не обязательная функция для скачивания картинок товаров
def download_card(url):
    resp = requests.get(url, stream=True)
    r = open("images\\" + url.split('/')[-1], "wb")
    for value in resp.iter_content(1048576):
        r.write(value)
    r.close()

# В данной функции мы получаем ссылку на карту с товаром с определенной страницы в диапазоне (1 - 6)
def get_url():
    for count in range(1, 7):
        link = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        responce = requests.get(link, headers=header).text
        soup = BeautifulSoup(responce, 'lxml')

        data = soup.find_all('div', class_="w-full rounded border")

        # В данном цикле находим ссылки на крты со страницы и передаем их через генератор поочереди
        # Это позволяет нам не забивать память, а выполнять код по мере необходимости
        for i in data:
            card_url = MAINLINK + i.find("a").get("href")
        yield card_url

# Основная функция для парсинга карты, которую получаем из функции get_url()
def pars_card():
    for card_url in get_url():
        responce = requests.get(card_url, headers=header).text
        sleep(3) # Здесь можно добавить ожидание, чтобы не нагружать сайт
        soup = BeautifulSoup(responce, 'lxml')
        data = soup.find('div', class_="my-8 w-full rounded border")

        name = data.find("h3", class_="card-title").text
        price = data.find("h4", class_="my-4 card-price").text
        description = data.find("p", class_="card-description").text
        img_link = MAINLINK + data.find("img").get("src")
        # Вызов функции для загрузки картинки данной карты товара (Не обязательно)
        download_card(img_link)
        # Возвращаем необходимые данные с помощью генератора
        yield name, price, description, img_link