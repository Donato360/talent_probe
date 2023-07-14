from  bs4 import BeautifulSoup
from helpers import Helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

SCROLL_PAUSE_TIME = 1

class ProfileOrganization(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.organizationItem = {
            "name": None,
            "start_date": None,
            "end_date": None,
            "summary": None
        }
        self.organizationList = []

    def resetOrganizationItem(self):
        self.organizationItem = {
            "name": None,
            "start_date": None,
            "end_date": None,
            "summary": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/organizations/'
        else:
            self.profileLink = self.profileLink + '/details/organizations/'

    def processOrganization(self, organizationItemArray):
        self.resetOrganizationItem()
        summary = []

        for index in range(len(organizationItemArray)):
            if index == 0:
                self.organizationItem['name'] = organizationItemArray[0]
            else:
                date = self.processDate(organizationItemArray[index])

                if date:
                    self.organizationItem['start_date'] = date['start_date']
                    self.organizationItem['end_date'] = date['end_date']
                else:
                    summary.append(organizationItemArray[index])

        if summary:
            self.organizationItem['summary'] = summary
        else:
            summary = None

        
        return self.organizationItem
    
    def getOrganization(self):
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

        try:
            organizations = source.select('li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated')
        except:
            organizations = None
        
        if organizations:
            for index, organization in enumerate(organizations):
                organization_text = organization.find_all('span', attrs={'aria-hidden':'true'})

                organization_item_array = []

                for index,text in enumerate(organization_text):
                    organization_item_array.append(text.getText())
                    
                    if index > 2:
                        break

                if not organization_item_array:
                    self.organizationList = None
                else:
                    self.organizationList.append(self.processOrganization(organization_item_array))
        else:
             self.organizationList = None

        profile_dictionary['organizations'] = self.organizationList

        return profile_dictionary
