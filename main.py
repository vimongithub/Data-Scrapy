import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import requests

chrome_driver_path = r"C:\Users\Vimal\Desktop\Python\Applications\chromedriver.exe"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfcA0kqp_L2dSCjBGJwp_cpvsJ8dCh0QZtKfdVTWgeZqKf5Ww/viewform?usp=sf_link"

# HOUSING_URL = "https://housing.com/rent/search-P6jqhmy6fy5snwxc7_o6tsq6mbi05buos_6acivvxo81lxg4br?listingId=9451574"
# header = {
#     "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
#     "Accept-Language" : "en-US,en;q=0.9,gu;q=0.8,hi;q=0.7"
# }
# response = requests.get(HOUSING_URL, headers=header)
# housing_html = response.text
#
# with open("housing_html.txt", mode='w', encoding="utf8") as file:
#     file.write(housing_html)

with open("housing_html.txt", mode='r', encoding="utf8") as file:
    data = file.read()

    soup = BeautifulSoup(data, "html.parser")
    price_html = soup.select('article .css-1cxwewr')
    price_list = [(price.text).replace(",","") for price in price_html]

    link_html = soup.select('.css-1ym6yxe')
    link_list = []
    for link in link_html:
        href = link["href"]
        if "http" not in href:
            link_list.append(f"https://housing.com/{href}")
        else:
            link_list.append(href)

    address_html = soup.select(".css-26olqx")
    address_list = [address.text for address in address_html]

    ser = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=ser)

    for number in range(len(address_list)):
        driver.get(url=GOOGLE_FORM_URL)
        time.sleep(5)

        address_field = driver.find_element(by=By.XPATH,
                                            value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_field = driver.find_element(by=By.XPATH,
                                          value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_field = driver.find_element(By.XPATH,
                                         value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit_btn = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

        address_field.send_keys(address_list[number])
        price_field.send_keys(price_list[number])
        link_field.send_keys(link_list[number])
        submit_btn.click()
        time.sleep(2)

    print("All data successfull saved in sheet")
