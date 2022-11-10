# -*- coding: utf-8 -*-

import re
import parameters
import time
from time import sleep
from selenium import webdriver
from  bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import numpy as np
import pandas as pd
import json
import argparse
import sys

SCROLL_PAUSE_TIME = 1

driver = webdriver.Chrome(ChromeDriverManager().install())

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Login
def login():
    driver.maximize_window()
    time.sleep(0.1)

    # login = open the file 'parameters.py' and edit your login details. This is your linkedin account login, store in a seperate text file. I recommend creating a fake account so your real one doesn't get flagged or banned
    email = parameters.username
    password = parameters.password

    driver.get("https://www.linkedin.com/login")
    time.sleep(0.2)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(0.2)


# Return profiles urls. User can upload profiles URLs from a linkedIn query, a python file or a csv file
def getProfileURLs(source):
    if source[0] == 'query':
        driver.get('https://www.google.com/')

        accept_google_cookies_button = driver.find_element(By.XPATH, '//button/div[contains(text(), "Accept all")]')
        accept_google_cookies_button.click()
        sleep(0.2)

        google_search_input = driver.find_element(By.XPATH, '//input[@name="q"]')
        google_search_input.send_keys(source[1])
        google_search_input.send_keys(Keys.RETURN)
        sleep(0.2)

        linkedin_profiles = driver.find_elements(By.XPATH, '//div/a[contains(@href,"linkedin.com/in/")]')
        linkedin_profiles = [profile.get_attribute('href') for profile in linkedin_profiles]
        return linkedin_profiles

    if source[0] == 'file':
        print(source[0])
        print(source[1])
        pass

    if source[0] == 'csv':
        print(source[0])
        print(source[1])
        pass
    
# parses a type 2 job row
def parseType2Jobs(alltext):
    jobgroups = []
    company = alltext[16][:len(alltext[16]) // 2]
    totalDurationAtCompany = alltext[20][:len(alltext[20]) // 2]

    # get rest of the jobs in the same nested list
    groups = []
    count = 0
    index = 0
    for a in alltext:
        if a == '' or a == ' ':
            count += 1
        else:
            groups.append((count, index))
            count = 0
        index += 1

    numJobsInJoblist = [g for g in groups if g[0] == 21 or g[0] == 22 or g[0] == 25 or g[0] == 26]
    for i in numJobsInJoblist:
        # full time/part time case
        if 'time' in alltext[i[1] + 5][:len(alltext[i[1] + 5]) // 2].lower().split('-'):
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 8][:len(alltext[i[1] + 8]) // 2]))
        else:
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 4][:len(alltext[i[1] + 4]) // 2]))
    return ('type2job', company, totalDurationAtCompany, jobgroups)

# parses a type 1 job row
def parseType1Job(alltext):
    jobtitle = alltext[16][:len(alltext[16]) // 2]
    company = alltext[20][:len(alltext[20]) // 2]
    duration = alltext[23][:len(alltext[23]) // 2]
    return ('type1job', jobtitle, company, duration)

# returns linkedin profile information
def returnProfileInfo(employeeLink):
    url = employeeLink
    driver.get(url)
    time.sleep(0.2)
    source = BeautifulSoup(driver.page_source, "html.parser")

    profile_dictionary = {}

    try:
        name_info = source.find('div', class_='mt2 relative')
        name = name_info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
    except:
        name = None

    profile_dictionary['full_name'] = name

    try:
        title = name_info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
    except:
        title = None

    profile_dictionary['job_title'] = title

    try:
        location = name_info.find('span' , {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
    except:
        location = None

    profile_dictionary['location_name'] = location
    
    time.sleep(0.1)
    experiences = source.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
    certification_list = []
    education_list = []
    skill_list = []

    for x in experiences[1:]:
        alltext = x.getText().split('\n')
        # print(alltext)
        startIdentifier = 0
        for e in alltext:
            if e == '' or e == ' ':
                startIdentifier+=1
            else:
                break
        # jobs, educations, certifications
        if startIdentifier == 16:
            # education
            if 'university' in alltext[16].lower().split(' ') or 'college' in alltext[16].lower().split(' ') or 'ba' in alltext[16].lower().split(' ') or 'bs' in alltext[16].lower().split(' '):
                education_list.append(('education', alltext[16][:len(alltext[16])//2], alltext[20][:len(alltext[20])//2]))

            # certifications
            elif 'issued' in alltext[23].lower().split(' '):
                certification_list.append(('certification', alltext[16][:len(alltext[16])//2], alltext[20][:len(alltext[20])//2]))

        elif startIdentifier == 12:
            # Skills
            if (alltext[16] == '' or alltext[16] == ' ') and len(alltext) > 24:
                skill_list.append(('skill', alltext[12][:len(alltext[12])//2]))

    if education_list:
        profile_dictionary['education'] = education_list

    if certification_list:
        profile_dictionary['certification'] = certification_list

    if skill_list:
        profile_dictionary['skills'] = skill_list

    # experiences
    url = driver.current_url + '/details/experience/'
    driver.get(url)
    time.sleep(0.2)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    source = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(0.1)
    exp = source.find_all('li', {"class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"})

    for e in exp:
        row = e.getText().split('\n')

        if row[:16] == ['', '', '', '', '', '', ' ', '', '', '', '', '', '', '', '', '']:
            if 'yrs' in row[25].split(' '):
                profile.append(parseType2Jobs(row))
            else:
                profile.append(parseType1Job(row))

    return profile_dictionary

if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    # Required positional argument
    parser.add_argument('--source', type=str, nargs=2, metavar=('[type]', '[query string, python file name or csv file name]'),
                     required=True, help='type of linkedIn profiles to process can be : "query", "file" or "csv"')

    args = parser.parse_args()

    login()

    linkedin_profiles = []
    
    linkedin_profiles = getProfileURLs(args.source)
    # linkedin_profiles = linkedin_profiles + ['https://www.linkedin.com/in/ykpgrr/', 'https://www.linkedin.com/in/lee-braybrooke-73666927/', 'https://www.linkedin.com/in/saman-nejad/', 'https://www.linkedin.com/in/eluert-mukja/', 'https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/']

    # linkedin_profiles = ['https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/']
    
    print(linkedin_profiles)
    
    profiles = []
    x = 1
    
    for profile in linkedin_profiles:
        profiles.append(returnProfileInfo(profile))

    with open('m&a.json', 'w') as f:
        json.dump(profiles, f)
    time.sleep(10)
    driver.quit()