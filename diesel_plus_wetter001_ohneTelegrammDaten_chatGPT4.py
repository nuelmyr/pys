import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import telebot
import time

# Telegram Bot-Token
bot_token = 

# Chat-ID
chat_id = 

# URLs der zu ladenden Bilder
image_urls = [
    "https://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_brd_uebermorgenspaet.jpg",
    "https://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_shh_uebermorgenspaet.jpg",
    "https://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_bay_uebermorgenspaet.jpg",
    "https://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_baw_uebermorgenspaet.jpg"
]

url_template = "https://www.fuelflash.eu/en/?land={}&suchfeld={}&entfernung=20&sorte={}&sortierung=preis"
params = [("de", "frankfurt", "diesel"),
          ("de", "heidelberg", "diesel"),
          ("de", "bielefeld", "diesel"),
          ("de", "neumünster", "diesel"),
          ("de", "hannover", "diesel"),
          ("de", "muenchen", "diesel"),
          ("fr", "nimes", "diesel"),
          ("es", "amposta", "diesel")
          ]

# Telegram-Bot initialisieren
bot = telebot.TeleBot(bot_token)

while True:
    for param_set in params:
        # generate the URL using the current set of parameters
        url = url_template.format(*param_set)

        # make the request and parse the HTML response
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # extract the first price element
        preis_elements = soup.find_all("span", {"class": "preis_part1"})[0]

        # extract the value of the "suchfeld" parameter from the URL
        parsed_url = urlparse(url)
        suchfeld_value = parse_qs(parsed_url.query)['suchfeld'][0]

        message = f"{suchfeld_value}: {preis_elements.text}"
        bot.send_message(chat_id, message)
        print(message)

        # Bilder herunterladen
    images = []
    for url in image_urls:
        response = requests.get(url)
        images.append(('image.jpg', response.content))

    # Bilder an Telegram-Bot senden
    for image in images:
        bot.send_photo(chat_id, photo=image)

    # wait for 60*x seconds before checking again
    time.sleep(60*30)
