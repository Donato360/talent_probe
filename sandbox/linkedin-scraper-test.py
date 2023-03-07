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
import numpy as np

SCROLL_PAUSE_TIME = 1

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(2)

accept_cookies_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]')
accept_cookies_button.click()

access_button = driver.find_element(By.XPATH, '//a[contains(text(), "Sign in")]')
access_button.click()
sleep(3)

username_input = driver.find_element(By.XPATH, '//input[@name="session_key"]')
username_input.send_keys(parameters.username)
sleep(0.5)
password_input = driver.find_element(By.XPATH, '//input[@name="session_password"]')
password_input.send_keys(parameters.password)
sleep(0.5)

signin_button = driver.find_element(By.XPATH, '//button[contains(text(), "Sign in")]')
signin_button.click()
sleep(0.5)

driver.get('https://www.google.com/')

accept_google_cookies_button = driver.find_element(By.XPATH, '//button/div[contains(text(), "Accept all")]')
accept_google_cookies_button.click()
sleep(0.5)

google_search_input = driver.find_element(By.XPATH, '//input[@name="q"]')
google_search_input.send_keys(parameters.search_query)
google_search_input.send_keys(Keys.RETURN)
sleep(1)

# linkedin_profiles = driver.find_elements(By.XPATH, '//div/a[contains(@href,"linkedin.com/in/")]')
# linkedin_profiles = [profile.get_attribute('href') for profile in linkedin_profiles]
linkedin_profiles = []
# linkedin_profiles.append('https://www.linkedin.com/in/ykpgrr/')
# linkedin_profiles.append('https://www.linkedin.com/in/lee-braybrooke-73666927/')
# linkedin_profiles.append('https://www.linkedin.com/in/saman-nejad/')
# linkedin_profiles.append('https://www.linkedin.com/in/eluert-mukja/')
linkedin_profiles.append('https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/')

print('\n')
print('********** PROFILES **********')
print('\n')

dictionary = {}
keys = ['name', 'profile', 'job_title', 'current_company', 'location', 'connections', 'summary', 'experience', 'education', 'licenses_and_certifications',
        'skills', 'endorsements', 'languages', 'publications', 'projects', 'organizations', 'telephone', 'email']

for profile in linkedin_profiles:
    start_time = time.time()
    values = []
    driver.get(profile)

    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(3):
        # scroll down to bottom
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # wait for page to load
        sleep(SCROLL_PAUSE_TIME)

        # calculate new scroll height with last scroll height
        new_height = driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        if new_height == last_height:
            break

        last_height = new_height

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        try:
            profile_div = soup.find('div', {'class': 'mt2 relative'})
            name = profile_div.find('h1' , {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
        except:
            name = 'data not found'

        try:
            job_title = profile_div.find('div' , {'class': 'text-body-medium break-words'}).get_text().strip()
        except:
            job_title = 'data not found'

        try:
            current_company = profile_div.find('div' , {'class': 'inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline'}).get_text().strip()
        except:
            current_company = 'data not found'

        try:
            location = profile_div.find('span' , {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
        except:
            location = 'data not found'

        try:
            connection_ul = soup.find('ul', {'class': 'pv-top-card--list pv-top-card--list-bullet display-flex pb1'})
            connections = connection_ul.find('span' , {'class': 't-bold'}).get_text().strip()
        except:
            connections = 'data not found'

        try:
            about_section = soup.find("div", {"id": "about"}).find_parent('section')
            summary = about_section.find_all('span' , {'class': 'visually-hidden'})[1].get_text().strip()
        except:
            summary = 'data not found'

        try:
            experience_section = soup.find("div", {"id": "experience"}).find_parent('section') 
            experience_div = experience_section.find("div", {"class": "pvs-list__outer-container"})
            experience_ul = experience_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            experience_li = experience_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            experience = []

            for index in range(len(experience_li)):
                visually_hidden_spans_in_experience_li = experience_li[index].find_all('span', {"class": "visually-hidden"})
                current_experience = []
                for span in visually_hidden_spans_in_experience_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_experience.append(text_in_visually_hidden_span)

                experience.append(current_experience)
        except:
            experience = 'data not found'

        try:
            education_section = soup.find("div", {"id": "education"}).find_parent('section')
            education_div =  education_section.find("div", {"class": "pvs-list__outer-container"})
            education_ul =  education_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            education_li =  education_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            education = []

            for index in range(len(education_li)):
                visually_hidden_spans_in_education_li = education_li[index].find_all('span', {"class": "visually-hidden"})
                current_education = []
                for span in visually_hidden_spans_in_education_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_education.append(text_in_visually_hidden_span)

                education.append(current_education)
        except:
            education = 'data not found'

        try:
            licenses_and_certifications_section = soup.find("div", {"id": "licenses_and_certifications"}).find_parent('section')
            licenses_and_certifications_div =  licenses_and_certifications_section.find("div", {"class": "pvs-list__outer-container"})
            licenses_and_certifications_ul =  licenses_and_certifications_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            licenses_and_certifications_li =  licenses_and_certifications_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            licenses_and_certifications = []

            for index in range(len(licenses_and_certifications_li)):
                visually_hidden_spans_in_licenses_and_certifications_li = licenses_and_certifications_li[index].find_all('span', {"class": "visually-hidden"})
                current_licenses_and_certifications = []
                for span in visually_hidden_spans_in_licenses_and_certifications_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_licenses_and_certifications.append(text_in_visually_hidden_span)

                licenses_and_certifications.append(current_licenses_and_certifications)
        except:
            licenses_and_certifications = 'data not found'

        try:
            skills_section = soup.find("div", {"id": "skills"}).find_parent('section')
            skills_div =  skills_section.find("div", {"class": "pvs-list__outer-container"})
            skills_ul =  skills_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            skills_li =  skills_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            skills = []
            endorsements = 0

            for index in range(len(skills_li)):
                visually_hidden_spans_in_skills_li = skills_li[index].find_all('span', {"class": "visually-hidden"})
                current_skills = []
                for span in visually_hidden_spans_in_skills_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    if 'endorsements' in text_in_visually_hidden_span:
                        int_array = [int(s) for s in str.split(text_in_visually_hidden_span) if s.isdigit()]
                        endorsements = endorsements + sum(int_array)
                    current_skills.append(text_in_visually_hidden_span)

                skills.append(current_skills)
        except:
            skills = 'data not found'
            endorsements = 'data not found'

        try:
            languages_section = soup.find("div", {"id": "languages"}).find_parent('section')
            languages_div =  languages_section.find("div", {"class": "pvs-list__outer-container"})
            languages_ul =  languages_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            languages_li =  languages_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            languages = []

            for index in range(len(languages_li)):
                visually_hidden_spans_in_languages_li = languages_li[index].find_all('span', {"class": "visually-hidden"})
                current_languages = []
                for span in visually_hidden_spans_in_languages_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_languages.append(text_in_visually_hidden_span)

                languages.append(current_languages)
        except:
            languages = 'data not found'

        try:
            publications_section = soup.find("div", {"id": "publications"}).find_parent('section')
            publications_div =  publications_section.find("div", {"class": "pvs-list__outer-container"})
            publications_ul =  publications_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            publications_li =  publications_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            publications = []

            for index in range(len(publications_li)):
                visually_hidden_spans_in_publications_li = publications_li[index].find_all('span', {"class": "visually-hidden"})
                current_publications = []
                for span in visually_hidden_spans_in_publications_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_publications.append(text_in_visually_hidden_span)

                publications.append(current_publications)
        except:
            publications = 'data not found'

        try:
            projects_section = soup.find("div", {"id": "projects"}).find_parent('section')
            projects_div =  projects_section.find("div", {"class": "pvs-list__outer-container"})
            projects_ul =  projects_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            projects_li =  projects_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            projects = []

            for index in range(len(projects_li)):
                visually_hidden_spans_in_projects_li = projects_li[index].find_all('span', {"class": "visually-hidden"})
                current_projects = []
                for span in visually_hidden_spans_in_projects_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_projects.append(text_in_visually_hidden_span)

                projects.append(current_projects)
        except:
            projects = 'data not found'

        try:
            organizations_section = soup.find("div", {"id": "organizations"}).find_parent('section')
            organizations_div =  organizations_section.find("div", {"class": "pvs-list__outer-container"})
            organizations_ul =  organizations_div.find("ul", {"class": "pvs-list ph5 display-flex flex-row flex-wrap"})
            organizations_li =  organizations_ul.find_all("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
            organizations = []

            for index in range(len(organizations_li)):
                visually_hidden_spans_in_organizations_li = organizations_li[index].find_all('span', {"class": "visually-hidden"})
                current_organizations = []
                for span in visually_hidden_spans_in_organizations_li:
                    text_in_visually_hidden_span = span.get_text().strip()
                    text_in_visually_hidden_span = text_in_visually_hidden_span.replace('\n',",")
                    current_organizations.append(text_in_visually_hidden_span)

                organizations.append(current_organizations)
        except:
            organizations = 'data not found'

    telephone = 'data not found'
    email = 'data not found'

    values = [name, profile, job_title, current_company,location, connections, summary, experience, education, licenses_and_certifications, 
        skills, endorsements, languages, publications, projects, organizations, telephone, email]

    dictionary = dict(zip(keys,values))

    # print(dictionary)    

    print('name:                        ', name)
    print('profile:                     ', profile)
    print('job_title:                   ', job_title)
    print('current_company:             ', current_company)
    print('location:                    ', location)
    print('connections:                 ', connections)
    print('summary:                     ', summary)
    print('experience:                  ', experience)
    print('education:                   ', education)
    print('licenses_and_certifications: ', licenses_and_certifications)
    print('skills:                      ', skills)
    print('endorsements:                ', endorsements)
    print('languages:                   ', languages)
    print('publications:                ', publications)
    print('projects:                    ', projects)
    print('organizations:               ', organizations)
    print('telephone:                   ', telephone)
    print('email:                       ', email)


    print('\n')
    print(time.time() - start_time, "seconds")
    print('_________________________________')
    print('\n')

# with open('single_profile_pretty.json', 'w') as fp:
#     json.dump(dictionary, fp, sort_keys=True, indent=4)

# with open('single_profile_raw.json', 'w') as fp:
#     json.dump(dictionary, fp)

    # with open('profiles_pretty.json', 'a') as fp:
    #     json.dump(dictionary, fp, sort_keys=True, indent=4)
    #     fp.write("\n")

    # with open('profiles_raw.json', 'a') as fp:
    #     json.dump(dictionary, fp)
    #     fp.write("\n")

# driver.quit()
