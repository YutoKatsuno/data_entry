from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import os
import re

# Get Environment variables
ACCEPT = os.environ["ACCEPT"]
ACCEPT_ENCODING = os.environ["ACCEPT_ENCODING"]
ACCEPT_LANGUAGE = os.environ["ACCEPT_LANGUAGE"]
CACHE_CONTROL = os.environ["CACHE_CONTROL"]
UPGRADE_INSECURE_REQUESTS = os.environ["UPGRADE_INSECURE_REQUESTS"]
USER_AGENT = os.environ["USER_AGENT"]
URL = os.environ["URL"]
GOOGLE_FORM = os.environ["GOOGLE_FORM"]
DRIVER_PATH = os.environ["DRIVER_PATH"]

# Define requests
headers = {
    'accept': ACCEPT,
    'accept-encoding': ACCEPT_ENCODING,
    'accept-language': ACCEPT_LANGUAGE,
    'cache-control': CACHE_CONTROL,
    'upgrade-insecure-requests': UPGRADE_INSECURE_REQUESTS,
    'user-agent': USER_AGENT,
}
response = requests.get(URL, headers=headers)

# Define BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# List to pass to Google form
link_list = []
price_list = []
address_list = []

# Make a list of links
link_data_list = soup.select("div.StyledPropertyCardPhotoBody-c11n-8-73-8__sc-128t811-0")
for link_data in link_data_list:
    link = link_data.select_one("a.property-card-link").get("href")
    link_list.append(f"https://www.zillow.com/{link}")

# Make a list of prices
price_data_list = soup.select("div.StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0.hRqIYX span")
for price_data in price_data_list:
    price = price_data.text
    price_list.append(re.split("[+/]", price)[0])

# Make a list of addresses
address_data_list = soup.select(
    "div.StyledPropertyCardDataWrapper-c11n-8-73-8__sc-1omp4c3-0.gXNuqr.property-card-data address")
for address_data in address_data_list:
    address = address_data.text
    address_list.append(address)

# Define selenium
chrome_service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service)
driver.get(GOOGLE_FORM)
time.sleep(3)

for address, price, link in zip(address_list, price_list, link_list):
    question_list = driver.find_elements(By.CSS_SELECTOR, "div.geS5n input")
    data_list = [address, price, link]
    for index, question in enumerate(question_list):
        question.send_keys(data_list[index], Keys.TAB)
        time.sleep(5)

