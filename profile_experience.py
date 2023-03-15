from  bs4 import BeautifulSoup
from time import sleep
from helpers import Helper

SCROLL_PAUSE_TIME = 1

class ProfileExperience(Helper):
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
        self.experienceItem = {
            "end_date": None,
            "summary": None,
            "location_names": [],
            "is_primary": False,
            "company": {
                "name": None,
                "location": {
                                'city': None,
                                'region': None,
                                'country': None
                            }
            },
            "title": {
                "name": None
            },
            "start_date": None
        }
        self.experienceList = []

    def resetExperienceItem(self):
        self.experienceItem = {
            "end_date": None,
            "summary": None,
            "location_names": [],
            "is_primary": False,
            "company": {
                "name": None,
                "location": {
                                'city': None,
                                'region': None,
                                'country': None
                            }
            },
            "title": {
                "name": None
            },
            "start_date": None
        }

    def processProfileLink(self):
        if self.profileLink[-1] == '/':
            self.profileLink = self.profileLink + 'details/experience/'
        else:
            self.profileLink = self.profileLink + '/details/experience/'

    def processJobType1(self, job_details_array):
        print('job type 1:')
        print()
        print('job_details_array: {}'.format(len(job_details_array)))
        print(job_details_array)
        print()
        dates = None
        locations = None
        summary = []

        self.experienceItem['title']['name'] = job_details_array[0]

        if len(job_details_array) == 2:
            self.experienceItem['company']['name'] = job_details_array[1]

        if len(job_details_array) == 3:
            self.experienceItem['company']['name'] = job_details_array[1]

            dates = self.processDate(job_details_array[2])

            if dates:
                self.experienceItem['start_date'] = dates['start_date']
                self.experienceItem['end_date'] = dates['end_date']

                if dates['end_date'] == 'present':
                    self.experienceItem['is_primary'] = True

        if len(job_details_array) == 4:        
            self.experienceItem['title']['name'] = job_details_array[0]
            self.experienceItem['company']['name'] = job_details_array[1]

            dates = self.processDate(job_details_array[2])

            if dates:
                self.experienceItem['start_date'] = dates['start_date']
                self.experienceItem['end_date'] = dates['end_date']

                if dates['end_date'] == 'present':
                    self.experienceItem['is_primary'] = True

            locations = self.processLocation(job_details_array[3])

            if locations:
                if locations['cities']:
                    self.experienceItem['company']['location']['city'] = ','.join(locations['cities'])
                if locations['regions']:
                    self.experienceItem['company']['location']['region'] = ','.join(locations['regions'])
                if locations['countries']:
                    self.experienceItem['company']['location']['country'] = ','.join(locations['countries'])
            else:
                summary.append(job_details_array[3])

        if len(job_details_array) >= 5:
            self.experienceItem['title']['name'] = job_details_array[0]
            self.experienceItem['company']['name'] = job_details_array[1]

            dates = self.processDate(job_details_array[2])

            if dates:
                self.experienceItem['start_date'] = dates['start_date']
                self.experienceItem['end_date'] = dates['end_date']

                if dates['end_date'] == 'present':
                    self.experienceItem['is_primary'] = True

            locations = self.processLocation(job_details_array[3])

            if locations:
                if locations['cities']:
                    self.experienceItem['company']['location']['city'] = ','.join(locations['cities'])
                if locations['regions']:
                    self.experienceItem['company']['location']['region'] = ','.join(locations['regions'])
                if locations['countries']:
                    self.experienceItem['company']['location']['country'] = ','.join(locations['countries'])

                for item in job_details_array[4:]:
                    summary.append(item)
            else:
                for item in job_details_array[3:]:
                    summary.append(item)

        if summary:
            self.experienceItem['summary'] = ','.join(summary)

        return self.experienceItem

    def processJobType2(self, job_details_array):
        print('process job type 2')
        print()

    def getExperience(self):
        self.processProfileLink()

        self.driver.get(self.profileLink)
        sleep(2)

        # Get scroll height after first time page load
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page / use a better technique like `waitforpageload` etc., if possible
            sleep(3)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        source = BeautifulSoup(self.driver.page_source, "html.parser")

        profile_dictionary = {}
        time_key_words_set = {'yrs', 'yr', 'mos', 'mo'}

        try:
            experiences = source.find_all('li', {"class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"})
            sleep(1)
        except:
            experiences = None

        if experiences:
            for index, experience in enumerate(experiences):
                self.resetExperienceItem()

                print('index: {}'.format(index))
                print()

                experience = experience.find_all('span', attrs={'aria-hidden':'true'})
                experience_item_array = []

                for index,text in enumerate(experience):
                    experience_item_array.append(text.getText())

                if not experience_item_array:
                    self.experienceList = None
                else:
                    type_job = 1

                    dates_string_set = set(experience_item_array[1].split())

                    if dates_string_set & time_key_words_set:
                        type_job = 2

                    if type_job == 1:
                        self.experienceList.append(self.processJobType1(experience_item_array))
                    else:
                        self.experienceList.append(self.processJobType2(experience_item_array))
        else:
             self.experienceList = None

        print()
        print('*****************************************************************')

        profile_dictionary['experience'] = self.experienceList

        return profile_dictionary