# -*- coding: utf-8 -*-

try:
    import re
    from parameters import username, password
    import time
    from time import sleep
    from datetime import datetime
    from selenium import webdriver
    from  bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from parsel import Selector
    from datetime import datetime
    import numpy as np
    import pandas as pd
    import json
    import argparse
    import sys
    from login import Login
    from profiles_urls import ProfileURLs
    from profile_general_info import ProfileGeneralInfo
    from helpers import average
    print('all module are loaded ')
    print()
except Exception as e:
    print('Error ->>>: {} '.format(e))
    print()

def main():
    SCROLL_PAUSE_TIME = 1

    try:
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        print('Driver: {} has been successfully set'.format(driver.name))
        print()
    except Exception as e:
        print('Webdriver not found')
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()

    try:
        # Instantiate the parser
        parser = argparse.ArgumentParser(description='Optional app description')

        # Required positional argument
        parser.add_argument('--source', type=str, nargs=2, metavar=('[type]', '[query string, python file name or csv file name]'),
                        required=True, help='type of linkedIn profiles to process can be : "profile", "query", "file" or "csv"')

        args = parser.parse_args()

        profileUrls_obj = ProfileURLs(driver, args.source)

        linkedin_profiles = profileUrls_obj.getProfileURLs()

        print('Found profile(s): {}'.format(linkedin_profiles))
        print()
    except Exception as e:
        print('Could not find profiles urls')
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()   

    try:
        login_url = 'https://www.linkedin.com/login'
        login_obj = Login(driver, login_url, username, password)
        login_obj.doLogin()
        print('Login to: {} was successfull'.format(login_url))
        print()
    except Exception as e:
        print('Could not login to {} '.format(login_url))
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()

    current_profile_execution_time = 0
    profiles_execution_times = []

    profiles = []
    x = 1
    
    for profile in linkedin_profiles:
        try:
            profileGeneralInfo_obj = ProfileGeneralInfo(driver, profile)
            start = time.time()

            profiles.append(profileGeneralInfo_obj.getGeneralInfo())

            end = time.time()

            current_profile_execution_time = (end-start) * 10**3
            profiles_execution_times.append(current_profile_execution_time)

            print('General Information for: {} was processed successfully'.format(profile))
            print()
        except Exception as e:
            print('Could not process profile: {} '.format(profile))
            print('Error ->>>: {} '.format(e))
            print()
            sys.exit()

    average_execution_time = average(profiles_execution_times)
    print("The average time of execution for a profile:", average_execution_time, "ms")

    now = datetime.now() # current date and time

    date_time = now.strftime("_%m_%d_%Y-%H_%M_%S")
    file_name = 'linkedInProfiles' + date_time + '.json'

    with open(file_name, 'w') as f:
        json.dump(profiles, f)
    
    driver.quit()

if __name__ == "__main__":
    main()