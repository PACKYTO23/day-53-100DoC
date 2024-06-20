import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ZILLOW_PAGE = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORMS = ("https://docs.google.com/forms/d/e/"
                "1FAIpQLSfMCcANj9U5UAVxuErmL9tvrEBQ78QoVH--7SWnpSFDQzC-sg/"
                "viewform?usp=sf_link")
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "es-419,es;q=0.9",
}

response = requests.get(url=ZILLOW_PAGE, headers=headers)
zillow_info = response.text
soup = BeautifulSoup(zillow_info, "html.parser")
info_list = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
price_data = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
address_list = []
price_list = []
link_list = []

for data in price_data:
    price_str = str(data)
    price = price_str.split(">")[1][:6]
    price_list.append(price)

price_list[14] = "$1,914"

for data in info_list:
    address = data.getText().strip()
    link = data.get("href")

    address_list.append(address)
    link_list.append(link)

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(GOOGLE_FORMS)

time.sleep(3)

address_response = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/'
                                                       'div[1]/div/div[1]/input')
price_response = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/'
                                                     'div[1]/div/div[1]/input')
link_response = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/'
                                                    'div[1]/div/div[1]/input')
send_button = driver.find_element(By.LINK_TEXT, value="Enviar")

for n in range(len(address_list)):
    address_response.send_keys(address_list[n])
    price_response.send_keys(price_list[n])
    link_response.send_keys(link_list[n])
    send_button.click()
    time.sleep(1)
