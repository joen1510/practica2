from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime

from dotenv import load_dotenv
import os
load_dotenv()
user = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')
hostname = os.getenv('MONGO_HOSTNAME')

uri = f"mongodb+srv://{user}:{password}@{hostname}/?retryWrites=true&w=majority"

mongo_client = MongoClient(uri, server_api=ServerApi('1'))


consulta = "chevrolet"

driver = webdriver.Chrome()
driver.get("https://ecuador.patiotuerca.com/")
search_box = driver.find_element(by=By.CSS_SELECTOR, value="#search-list")

search_box.send_keys(consulta)

search_button = driver.find_element(by=By.CSS_SELECTOR, value="#openSearch > div > div > div.search-ots.false > img")
search_button.click()

vehicle_cards = driver.find_elements(By.CSS_SELECTOR, "#featuredUsed > div.xl3")


for card in vehicle_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > div.module.tittle").text
        kms_y_city = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > div.latam-secondary-text.text-lighten-2.left.vehicle-highlight").text
        price = card.find_element(By.CSS_SELECTOR, "div > div > div > div.card-info.card-content > strong").text
        print(title)
        print(kms_y_city)
        print(f"${price}")

        coche_actual = {
            "consulta": consulta,
            "resultado": {
                "title": title,
                "kms_y_city": kms_y_city,
                "price": price,
            }
        }

        db = mongo_client.get_database('db_eig')
        collection = db.get_collection(f'chevrolet')

        collection.insert_one(coche_actual)

        print("++++++++++++++++++++++++++++++++")
    except Exception as e:
        print(e)
        print("++++++++++++++++++++++++++++++++")


driver.close()
