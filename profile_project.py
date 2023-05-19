from  bs4 import BeautifulSoup
from helpers import Helper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

SCROLL_PAUSE_TIME = 1

class ProfileProject(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.projectItem = {
            "name": None,
            "start_date": None,
            "end_date": None,
            "project_url": None,
            "summary": None
        }
        self.projectList = []

    def resetProjectItem(self):
        self.projectItem = {
            "name": None,
            "start_date": None,
            "end_date": None,
            "project_url": None,
            "summary": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/projects/'
        else:
            self.profileLink = self.profileLink + '/details/projects/'

    def processProject(self, projectItemArray, project_link):
        self.resetProjectItem()
        summary = []

        for index in range(len(projectItemArray)):
            if index == 0:
                self.projectItem['name'] = projectItemArray[0]
            else:
                date = self.processDate(projectItemArray[index])

                if date:
                    self.projectItem['start_date'] = date['start_date']
                    self.projectItem['end_date'] = date['end_date']
                else:
                    summary.append(projectItemArray[index])
        if summary:
            self.projectItem['summary'] = summary
        else:
            summary = None

        self.projectItem['project_url'] = project_link
        
        return self.projectItem
    
    def getProject(self):
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
            projects = source.select('li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated')
        except:
            projects = None
        
        if projects:
            for index, project in enumerate(projects):
                project_text = project.find_all('span', attrs={'aria-hidden':'true'})
                project_link = project.find('a', class_= ['optional-action-target-wrapper artdeco-button artdeco-button--secondary artdeco-button--standard artdeco-button--2 artdeco-button--muted inline-flex justify-center align-self-flex-start'])
                if project_link:
                    project_link = project_link.get('href')
                else:
                    project_link = None

                project_item_array = []

                for index,text in enumerate(project_text):
                    project_item_array.append(text.getText())
                    
                    if index > 2:
                        break

                if not project_item_array:
                    self.projectList = None
                else:
                    self.projectList.append(self.processProject(project_item_array, project_link))
        else:
             self.projectList = None

        profile_dictionary['projects'] = self.projectList

        return profile_dictionary
