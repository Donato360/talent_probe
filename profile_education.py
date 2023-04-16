from  bs4 import BeautifulSoup
from helpers import Helper

SCROLL_PAUSE_TIME = 1

class ProfileEducation(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.educationItem = {
            "school": {
                "name": None
            },
            "end_date": None,
            "start_date": None,
            "degrees": []
        }
        self.educationList = []

    def resetEducationItem(self):
        self.educationItem = {
            "school": {
                "name": None
            },
            "end_date": None,
            "start_date": None,
            "degrees": []
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/education/'
        else:
            self.profileLink = self.profileLink + '/details/education/'

    def processEducation(self, educationItemArray):
        self.resetEducationItem()
        
        if len(educationItemArray) == 2:
            dates = self.processDate(educationItemArray[1])

            if dates:
                self.educationItem['school'] = educationItemArray[0]
                self.educationItem['start_date'] = dates['start_date']
                self.educationItem['end_date'] = dates['end_date']
            else:
                self.educationItem['school'] = educationItemArray[0]
                self.educationItem['degrees'].append(educationItemArray[1])

        if len(educationItemArray) >= 3:
            datePosition = -1

            dates2 = self.processDate(educationItemArray[2])
            if dates2:
                datePosition = 2

            dates1 = self.processDate(educationItemArray[1])
            if dates1:
                datePosition = 1

            if datePosition == 2:
                self.educationItem['school'] = educationItemArray[0]
                self.educationItem['degrees'].append(educationItemArray[1])
                self.educationItem['start_date'] = dates2['start_date']
                self.educationItem['end_date'] = dates2['end_date']

            if datePosition == 1:
                self.educationItem['school'] = educationItemArray[0]
                self.educationItem['degrees'].append(educationItemArray[2])
                self.educationItem['start_date'] = dates1['start_date']
                self.educationItem['end_date'] = dates1['end_date']
            
            if datePosition == -1:
                self.educationItem['school'] = educationItemArray[0]
                self.educationItem['degrees'].append(educationItemArray[1])

        return self.educationItem
    
    def getEducation(self):
        self.processProfileLink()

        self.driver.get(self.profileLink)

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
            educations = source.find_all('li', class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated')
        except:
            educations = None
        
        if educations:
            for index, education in enumerate(educations):
                # print('index: {}'.format(index))

                education = education.find_all('span', attrs={'aria-hidden':'true'})
                education_item_array = []

                for index,text in enumerate(education):
                    education_item_array.append(text.getText())
                    
                    if index > 2:
                        break

                if not education_item_array:
                    self.educationList = None
                else:
                    self.educationList.append(self.processEducation(education_item_array))
        else:
             self.educationList = None
             
        # print(self.educationList)
        # print()
        # print('*****************************************************************')

        profile_dictionary['education'] = self.educationList

        return profile_dictionary
