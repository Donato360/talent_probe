from  bs4 import BeautifulSoup
from time import sleep
from helpers import Helper

SCROLL_PAUSE_TIME = 1

class ProfileEducation(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/education/'
        else:
            self.profileLink = self.profileLink + '/details/education/'
    
    def getEducation(self):
        self.processProfileLink()

        self.driver.get(self.profileLink)
        sleep(0.1)

        # Get scroll height after first time page load
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page / use a better technique like `waitforpageload` etc., if possible
            sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        source = BeautifulSoup(self.driver.page_source, "html.parser")

        profile_dictionary = {}
        education_list = []
        dates = {}
        degree = []
        school = None
        start_date = None
        end_date = None
        degrees = None
        datePosition = 0

        try:
            educations = source.find_all('li', {"class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"})
            sleep(0.1)
        except:
            educations = None
        
        if educations:
            for education in educations:
                alltext = education.getText().split('\n')
                alltext = [x.strip() for x in alltext if x.strip()]
                
                if alltext:
                    for index, text in enumerate(alltext):
                        dates =  self.processDate(text)

                        if dates['start_date'] or dates['end_date']:
                            print('datePosition: {}'.format(index))
                            print('string containing date: {}'.format(text))
                            print('*****************************************************************')
                            break

                # try:
                #     if alltext[1]:
                #         self.aDate = alltext[1]
                #         dates = self.processDate()
                #         datePosition = 1
                # except:
                #     pass

                # try:
                #     if alltext[2]:
                #         self.aDate = alltext[2]
                #         dates = self.processDate()
                #         datePosition = 2
                # except:
                #     pass

                # print(datePosition)

                # if datePosition == 0:
                #     start_date = None
                #     end_date = None
                #     degree.append(alltext[1])
                # else:
                #     if datePosition == 1:
                #         if len(dates) == 1:
                #             start_date = None
                #             end_date = dates[0]
                #             degree.append(None)
                #         else:
                #             start_date = dates[0]
                #             end_date = dates[1]
                #             degree.append(None)

                #     if datePosition == 2:
                #         if len(dates) == 1:
                #             start_date = None
                #             end_date = dates[0]
                #             degree.append(alltext[1])
                #         else:
                #             start_date = dates[0]
                #             end_date = dates[1]
                #             degree.append(alltext[1])
                
                # education_details = {"school": {'name': alltext[0]},
                #                         'end_date': end_date,
                #                         'start_date': start_date,
                #                         'degrees': ['']
                #                     }
                
                education_details = {"school": {'name': school},
                                        'end_date': end_date,
                                        'start_date': start_date,
                                        'degrees': [degrees]
                                    }
                
                education_list.append(education_details)
        
        profile_dictionary['education'] = education_list

        return profile_dictionary
