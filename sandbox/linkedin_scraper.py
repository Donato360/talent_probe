# -*- coding: utf-8 -*-

try:
    import re
    import parameters
    import time
    from time import sleep
    from datetime import datetime
    from selenium import webdriver
    from  bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import seleniumwire.undetected_chromedriver as uc
    from parsel import Selector
    from datetime import datetime
    import numpy as np
    import pandas as pd
    import json
    import argparse
    import sys
    import os
    print('All modules are loaded ')
    print()
except Exception as e:
    print('Libraries Load Error ->>>: {} '.format(e))
    print()

class ProfileURLs:
    def __init__(self, driver, source):
        self.driver = driver
        self.source = source

    def getProfileURLs(self):
        if self.source[0] == 'query':
            self.driver.get('https://www.google.com/')

            accept_google_cookies_button = self.driver.find_element(By.XPATH, '//button/div[contains(text(), "Accept all")]')
            accept_google_cookies_button.click()

            google_search_input = self.driver.find_element(By.XPATH, '//input[@name="q"]')
            google_search_input.send_keys(self.source[1])
            google_search_input.send_keys(Keys.RETURN)

            linkedin_profiles = self.driver.find_elements(By.XPATH, '//div/a[contains(@href,"linkedin.com/in/")]')
            linkedin_profiles = [profile.get_attribute('href') for profile in linkedin_profiles]

        if self.source[0] == 'profile':
            linkedin_profiles = [self.source[1]]
            
        if self.source[0] == 'file':
            print(self.source[0])
            print(self.source[1])

        if self.source[0] == 'csv':
            print(self.source[0])
            print(self.source[1])
            pass

        return linkedin_profiles

class Login:
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def doLogin(self):
        try:
            self.driver.maximize_window()
            time.sleep(0.1)

            print(self.url)
            self.driver.get(self.url)
            self.driver.implicitly_wait(3)

            eml = self.driver.find_element(by=By.ID, value="username")
            eml.send_keys(self.username)
            passwd = self.driver.find_element(by=By.ID, value="password")
            passwd.send_keys(self.password)
            loginbutton = self.driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
            loginbutton.click()
            return('Successfull login: {} '.format(self.url))
        except Exception as e:
            return('Login error ->>>: {} '.format(e))

def main():
    SCROLL_PAUSE_TIME = 1

    os.environ['WDM_SSL_VERIFY'] = '0'

    print(os.path.dirname(os.path.abspath(__file__)))

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--allow-insecure-localhost')

    options = {
        'ca_cert': '/Volumes/SAM_Backup/data_scraping/linkedIn_data_scraper/ca.crt'
    }

    driver = uc.Chrome(
        options=chrome_options,
        seleniumwire_options=options
    )

    url = "https://www.google.com/"

    driver.get(url)

    # options = Options()
    # # options.add_argument("--headless")
    # options.add_experimental_option("detach", True)

    # options = {
    #     'ca_cert': '/ca.crt'
    # }
    
    # chrome_options = uc.ChromeOptions()

    # driver = uc.Chrome(
    #     options=chrome_options,
    #     seleniumwire_options=options
    # )

    # # Instantiate the parser
    # parser = argparse.ArgumentParser(description='Optional app description')

    # # Required positional argument
    # parser.add_argument('--source', type=str, nargs=2, metavar=('[type]', '[query string, python file name or csv file name]'),
    #                  required=True, help='type of linkedIn profiles to process can be : "profile", "query", "file" or "csv"')

    # args = parser.parse_args()

    # objProfiles = ProfileURLs(driver, args.source)
    # linkedin_profiles = objProfiles.getProfileURLs()
    # time.sleep(0.1)

    # url = "https://www.linkedin.com/login"

    # if linkedin_profiles:
    #     objLogin = Login(driver, url, parameters.username, parameters.password)
    #     print(objLogin.doLogin())
    #     print()
    # else:
    #     print('No profile(s) found')
    #     print()

    time.sleep(1)

if __name__ == "__main__":
    main()