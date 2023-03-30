from bs4 import BeautifulSoup, NavigableString, Tag
from time import sleep
from helpers import Helper
import copy

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
        self.experienceItems = []

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
                    self.experienceItem['company']['location']['city'] = ','.join(
                        locations['cities'])
                if locations['regions']:
                    self.experienceItem['company']['location']['region'] = ','.join(
                        locations['regions'])
                if locations['countries']:
                    self.experienceItem['company']['location']['country'] = ','.join(
                        locations['countries'])
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
                    self.experienceItem['company']['location']['city'] = ','.join(
                        locations['cities'])
                if locations['regions']:
                    self.experienceItem['company']['location']['region'] = ','.join(
                        locations['regions'])
                if locations['countries']:
                    self.experienceItem['company']['location']['country'] = ','.join(
                        locations['countries'])

                for item in job_details_array[4:]:
                    summary.append(item)
            else:
                for item in job_details_array[3:]:
                    summary.append(item)

        if summary:
            self.experienceItem['summary'] = ','.join(summary)

        return self.experienceItem

    def processJobType2(self, experience):
        # print('job type 2:')
        # print()
        experience_decomposed = copy.copy(experience)

        for ul in experience_decomposed('ul'):
            ul.decompose()

        for index, span in enumerate(experience_decomposed.find_all('span', attrs={'aria-hidden': 'true'})):
            if index == 0:
                company_name = span.getText().strip()
            else:
                locations_general = self.processLocation(span.getText())

                if locations_general:
                    if locations_general['cities']:
                        self.experienceItem['company']['location']['city'] = ','.join(
                            locations_general['cities'])
                    if locations_general['regions']:
                        self.experienceItem['company']['location']['region'] = ','.join(
                            locations_general['regions'])
                    if locations_general['countries']:
                        self.experienceItem['company']['location']['country'] = ','.join(
                            locations_general['countries'])

        # print('company_name: {}'.format(company_name))
        # print('city: {}'.format(
        #     self.experienceItem['company']['location']['city']))
        # print('region: {}'.format(
        #     self.experienceItem['company']['location']['region']))
        # print('country: {}'.format(
        #     self.experienceItem['company']['location']['country']))

        # print()

        for li_tag in experience.find('ul', {'class': 'pvs-list'}):

            if isinstance(li_tag, NavigableString):
                continue

            self.resetExperienceItem()

            for span_tag in li_tag.find_all('li', {'class': 'pvs-list__paged-list-item'}):
                experience_item_array = []
                experience_2 = span_tag.find_all(
                    'span', attrs={'aria-hidden': 'true'})

                for index, text in enumerate(experience_2):
                    experience_item_array.append(text.getText())

                dates_1 = None
                dates_2 = None
                locations_1 = None
                locations_2 = None

                summary = []

                self.experienceItem['title']['name'] = experience_item_array[0]

                if len(experience_item_array) == 2:
                    dates_1 = self.processDate(experience_item_array[1])
                    locations_1 = self.processLocation(
                        experience_item_array[1])

                    if (not dates_1) and (not locations_1):
                        if locations_general:
                            if locations_general['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(
                                    locations_general['cities'])
                            if locations_general['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(
                                    locations_general['regions'])
                            if locations_general['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(
                                    locations_general['countries'])
                                
                        for item in experience_item_array[1:]:
                            summary.append(item)

                    if (not dates_1) and (locations_1):
                        # print(locations_1)
                        if len(experience_item_array[1].split() <= 6):
                            if locations_1['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(
                                    locations_1['cities'])
                            if locations_1['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(
                                    locations_1['regions'])
                            if locations_1['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(
                                    locations_1['countries'])
                        else:
                            for item in experience_item_array[1:]:
                                summary.append(item)

                    if (dates_1) and (not locations_1):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']
                    
                    if (dates_1) and (locations_1):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                    # print('dates_1 = 2', dates_1)
                    # print('dates_2 = 2', dates_2)
                    # print('locations_1 = 2', locations_1)
                    # print('locations_2 = 2', locations_2)
                    # print()
                    # print(experience_item_array)
                    # print()

                if len(experience_item_array) > 2:
                    dates_1 = self.processDate(experience_item_array[1])
                    dates_2 = self.processDate(experience_item_array[2])
                    locations_1 = self.processLocation(
                        experience_item_array[1])
                    locations_2 = self.processLocation(
                        experience_item_array[2])

                    if (not dates_1) and (not dates_2) and (not locations_1) and (not locations_2):
                        if locations_general:
                            if locations_general['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_general['cities'])
                            if locations_general['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_general['regions'])
                            if locations_general['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_general['countries'])

                        try:
                            for item in experience_item_array[1:]:
                                summary.append(item)
                        except Exception:
                            pass
                        
                    if (not dates_1) and (not dates_2) and (not locations_1) and (locations_2):
                        if len(experience_item_array[2].split()) <= 4:
                            if locations_2['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_2['cities'])
                            if locations_2['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_2['regions'])
                            if locations_2['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_2['countries'])

                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[1:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (not dates_1) and (not dates_2) and (locations_1) and (not locations_2):
                        if len(experience_item_array[1].split()) <= 4:
                            if locations_1['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_1['cities'])
                            if locations_1['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_1['regions'])
                            if locations_1['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_1['countries'])

                            try:
                                for item in experience_item_array[2:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[1:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (not dates_1) and (not dates_2) and (locations_1) and (locations_2):
                        if len(experience_item_array[1].split()) <= 4:
                            if locations_1['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_1['cities'])
                            if locations_1['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_1['regions'])
                            if locations_1['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_1['countries'])

                            try:
                                for item in experience_item_array[2:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            if len(experience_item_array[2].split()) <= 4:
                                if locations_2['cities']:
                                    self.experienceItem['company']['location']['city'] = ','.join(locations_2['cities'])
                                if locations_2['regions']:
                                    self.experienceItem['company']['location']['region'] = ','.join(locations_2['regions'])
                                if locations_2['countries']:
                                    self.experienceItem['company']['location']['country'] = ','.join(locations_2['countries'])

                                try:
                                    for item in experience_item_array[3:]:
                                        summary.append(item)
                                except Exception:
                                    pass
                            else:
                                try:
                                    for item in experience_item_array[1:]:
                                        summary.append(item)
                                except Exception:
                                    pass

                    if (not dates_1) and (dates_2) and (not locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_2['start_date']
                        self.experienceItem['end_date'] = dates_2['end_date']

                        locations_3 = self.processLocation(experience_item_array[2])

                        if len(experience_item_array[3].split()) <= 4:
                            if locations_3['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_3['cities'])
                            if locations_3['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_3['regions'])
                            if locations_3['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_3['countries'])

                            try:
                                for item in experience_item_array[4:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (not dates_1) and (dates_2) and (not locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_2['start_date']
                        self.experienceItem['end_date'] = dates_2['end_date']

                        locations_3 = self.processLocation(experience_item_array[2])

                        if len(experience_item_array[3].split()) <= 4:
                            if locations_3['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_3['cities'])
                            if locations_3['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_3['regions'])
                            if locations_3['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_3['countries'])

                            try:
                                for item in experience_item_array[4:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (not dates_1) and (dates_2) and (locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_2['start_date']
                        self.experienceItem['end_date'] = dates_2['end_date']

                        if len(experience_item_array[1].split()) <= 4:
                            if locations_1['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_1['cities'])
                            if locations_1['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_1['regions'])
                            if locations_1['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_1['countries'])

                        try:
                            for item in experience_item_array[3:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (not dates_1) and (dates_2) and (locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_2['start_date']
                        self.experienceItem['end_date'] = dates_2['end_date']

                        if len(experience_item_array[1].split()) <= 4:
                            if locations_1['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_1['cities'])
                            if locations_1['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_1['regions'])
                            if locations_1['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_1['countries'])

                        try:
                            for item in experience_item_array[3:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (dates_1) and (not dates_2) and (not locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        try:
                            for item in experience_item_array[2:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (dates_1) and (not dates_2) and (not locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        if len(experience_item_array[2].split()) <= 4:
                            if locations_2['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_2['cities'])
                            if locations_2['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_2['regions'])
                            if locations_2['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_2['countries'])

                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[2:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (dates_1) and (not dates_2) and (locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        try:
                            for item in experience_item_array[2:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (dates_1) and (not dates_2) and (locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        if len(experience_item_array[2].split()) <= 4:
                            if locations_2['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_2['cities'])
                            if locations_2['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_2['regions'])
                            if locations_2['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_2['countries'])

                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[2:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (dates_1) and (dates_2) and (not locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        try:
                            for item in experience_item_array[2:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (dates_1) and (dates_2) and (not locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        if len(experience_item_array[2].split()) <= 4:
                            if locations_2['cities']:
                                self.experienceItem['company']['location']['city'] = ','.join(locations_2['cities'])
                            if locations_2['regions']:
                                self.experienceItem['company']['location']['region'] = ','.join(locations_2['regions'])
                            if locations_2['countries']:
                                self.experienceItem['company']['location']['country'] = ','.join(locations_2['countries'])

                            try:
                                for item in experience_item_array[3:]:
                                    summary.append(item)
                            except Exception:
                                pass
                        else:
                            try:
                                for item in experience_item_array[2:]:
                                    summary.append(item)
                            except Exception:
                                pass

                    if (dates_1) and (dates_2) and (locations_1) and (not locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        try:
                            for item in experience_item_array[2:]:
                                summary.append(item)
                        except Exception:
                            pass

                    if (dates_1) and (dates_2) and (locations_1) and (locations_2):
                        self.experienceItem['start_date'] = dates_1['start_date']
                        self.experienceItem['end_date'] = dates_1['end_date']

                        try:
                            for item in experience_item_array[2:]:
                                summary.append(item)
                        except Exception:
                            pass

                if summary:
                    self.experienceItem['summary'] = ','.join(summary)

                # print(self.experienceItem)
                # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

                self.experienceItems.append(self.experienceItem)

        return self.experienceItems

    def getExperience(self):
        self.processProfileLink()

        self.driver.get(self.profileLink)
        # sleep(2)

        # Get scroll height after first time page load
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page / use a better technique like `waitforpageload` etc., if possible
            # sleep(3)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        source = BeautifulSoup(self.driver.page_source, "html.parser")

        profile_dictionary = {}
        time_key_words_set = {'yrs', 'yr', 'mos', 'mo'}

        try:
            experiences = source.find_all(
                'li', {"class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated"})
            # sleep(1)
        except:
            experiences = None

        if experiences:
            for index, experience in enumerate(experiences):
                self.resetExperienceItem()

                # print('index: {}'.format(index))
                # print()

                experience_1 = experience.find_all(
                    'span', attrs={'aria-hidden': 'true'})
                experience_item_array = []

                for index, text in enumerate(experience_1):
                    experience_item_array.append(text.getText())

                if not experience_item_array:
                    self.experienceList = None
                else:
                    type_job = 1

                    dates_string_set = set(experience_item_array[1].split())

                    if dates_string_set & time_key_words_set:
                        type_job = 2

                    if type_job == 1:
                        self.experienceList.append(
                            self.processJobType1(experience_item_array))
                    else:
                        self.experienceList.append(self.processJobType2(experience))
        else:
            self.experienceList = None

        # print()
        # print('*****************************************************************')

        profile_dictionary['experience'] = self.experienceList

        return profile_dictionary
