from  bs4 import BeautifulSoup
from helpers import Helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re

SCROLL_PAUSE_TIME = 1

class ProfileSkill(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.skillItem = {
            "name": None,
            "endorsements": None
        }
        self.skillList = []

    def resetSkillItem(self):
        self.skillItem = {
            "name": None,
            "endorsements": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/skills/'
        else:
            self.profileLink = self.profileLink + '/details/skills/'

    def getSkill(self):
        self.processProfileLink()

        self.driver.get(self.profileLink)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main')))
        except TimeoutException:
            print("Timed out, couldn't load the page {} in time".format(self.profileLink))
            self.driver.quit()

        # Get scroll height after first time page load
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="globalfooter-about"]')))
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        source = BeautifulSoup(self.driver.page_source, 'lxml')

        profile_dictionary = {}
        text = 'Skills'

        skills_section = source.find(lambda tag: tag.name == "h2" and text in tag.text).find_parent('section')
        skills_li = skills_section.find('ul', class_= ['pvs-list']).findChildren('li', recursive=False)
        
        self.skillList = []

        if skills_li:
            for li in skills_li:
                current_skill = []

                for el in li.find_all('span', {"class": "visually-hidden"}):
                    current_skill.append(el.get_text())

                if current_skill:
                    self.resetSkillItem()

                    self.skillItem['name'] = current_skill[0]

                    if len(current_skill) > 1:
                        for item in current_skill[1:]:
                            if 'endorsements' in item:
                                self.skillItem['endorsements'] = current_skill[1]
                                break

                    self.skillList.append(self.skillItem)
        
        if self.skillList:
            profile_dictionary['skills'] = self.skillList
        else:
            profile_dictionary['skills'] = None

        return profile_dictionary
