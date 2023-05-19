from  bs4 import BeautifulSoup
from helpers import Helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

SCROLL_PAUSE_TIME = 1

class ProfileCertification(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.certificationItem = {
            "name": None,
            "organization": None,
            "issued_date": None,
            "credential_id": None,
            "certificate_url": None
        }
        self.certificationList = []

    def resetCertificationItem(self):
        self.certificationItem = {
            "name": None,
            "organization": None,
            "issued_date": None,
            "credential_id": None,
            "certificate_url": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/certifications/'
        else:
            self.profileLink = self.profileLink + '/details/certifications/'

    def processCertification(self, certificationItemArray, certification_link):
        self.resetCertificationItem()

        for index in range(len(certificationItemArray)):
            if index == 0:
                self.certificationItem['name'] = certificationItemArray[0]
            elif index == 1:
                self.certificationItem['organization'] = certificationItemArray[1]
            elif index == 2:
                issued_date = self.processDate(certificationItemArray[2])

                if issued_date:
                    self.certificationItem['issued_date'] = issued_date['end_date']
            elif index == 3:
                self.certificationItem['credential_id'] = certificationItemArray[3]
            
        self.certificationItem['certificate_url'] = certification_link
        
        return self.certificationItem
    
    def getCertification(self):
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

        try:
            certifications = source.select('li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated')
        except:
            certifications = None
        
        if certifications:
            for index, certification in enumerate(certifications):
                certification_text = certification.find_all('span', attrs={'aria-hidden':'true'})
                certification_link = certification.find('a', class_= ['optional-action-target-wrapper artdeco-button artdeco-button--secondary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center align-self-flex-start'])
                if certification_link:
                    certification_link = certification_link.get('href')
                else:
                    certification_link = None

                certification_item_array = []

                for index,text in enumerate(certification_text):
                    certification_item_array.append(text.getText())
                    
                    if index > 2:
                        break

                if not certification_item_array:
                    self.certificationList = None
                else:
                    self.certificationList.append(self.processCertification(certification_item_array, certification_link))
        else:
             self.certificationList = None

        profile_dictionary['licenses&certifications'] = self.certificationList

        return profile_dictionary
