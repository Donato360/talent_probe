from  bs4 import BeautifulSoup
from helpers import Helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re

SCROLL_PAUSE_TIME = 1

class ProfileLanguage(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.languageItem = {
            "name": None,
            "proficiency": None
        }
        self.languageList = []

    def resetLanguageItem(self):
        self.languageItem = {
            "name": None,
            "proficiency": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/languages/'
        else:
            self.profileLink = self.profileLink + '/details/languages/'

    def getLanguage(self):
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
            # Wait to load page / use a better technique like `waitforpageload` etc., if possible
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        source = BeautifulSoup(self.driver.page_source, 'lxml')

        profile_dictionary = {}
        text = 'Languages'

        languages_section = source.find(lambda tag: tag.name == "h2" and text in tag.text).find_parent('section')
        languages_li = languages_section.find_all('li', class_= ['pvs-list__paged-list-item', 'artdeco-list__item pvs-list__item--line-separated', 'pvs-list__item--one-column'])
        languages = []
        self.languageList = []

        if languages_li:
            for index in range(len(languages_li)):
                current_language = []
                for el in languages_li[index].find_all('span', {"class": "visually-hidden"}):
                    current_language.append(el.get_text())

                if current_language:
                    self.resetLanguageItem()

                    self.languageItem['name'] = current_language[0]
                    self.languageItem['proficiency'] = current_language[1]

                    self.languageList.append(self.languageItem)
        
        if self.languageList:
            profile_dictionary['languages'] = self.languageList
        else:
            profile_dictionary['languages'] = None

        return profile_dictionary
