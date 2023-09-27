from contextlib import closing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import pickle
import os
import time
import csv
from pathlib import Path

# set up Chrome driver
# Get the current working directory
cwd = os.getcwd()  
# Set the ChromeDriver executable path
driver_path = os.path.join(cwd, "chromedriver-linux64/chromedriver") 
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

with closing(webdriver.Chrome(service=service, options=options)) as driver:
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

# navigate to amazon homepage
driver.get('https://www.amazon.com/')

# find searchbar and input
title_element = driver.find_element("id", "twotabsearchtextbox")
title_element.send_keys("apple macbook")
driver.find_element("id", "nav-search-submit-button").click()
time.sleep(10)

response = driver.page_source
soup = BeautifulSoup(response, 'html.parser')

products = soup.findAll("div", class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis s-latency-cf-section s-card-border")

# scrape results
for product in products:
    try:
        name = product.find("span", class_="a-size-medium a-color-base a-text-normal").text
    except Exception as ex:
        name = ""
    try:
        price = product.find("span", class_="a-price-whole").text
    except Exception as ex:
        price = ""

    exist = Path('/amazon_scrape/amazon.csv').is_file()
    if not exist:
        with open('/amazon_scrape/amazon.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["name", "price"])
    print(name, price)
    with open('amazon.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, price])

# quit driver
driver.quit()