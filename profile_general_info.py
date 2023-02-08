from  bs4 import BeautifulSoup
from time import sleep

SCROLL_PAUSE_TIME = 1

class ProfileGeneralInfo:
    def __init__(self, driver, profileLink):
        self.driver = driver
        self.profileLink = profileLink
    
    def getGeneralInfo(self):
        self.driver.get(self.profileLink)
        sleep(0.2)

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

        try:
            name_info = source.find('div', class_='mt2 relative')
            name = name_info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
        except:
            name = None

        profile_dictionary['full_name'] = name

        try:
            forename = name.rsplit(' ', 1)[0]
        except:
            forename = None

        profile_dictionary['first_name'] = forename

        try:
            name_components = name.split()
            surname = name_components[-1]
        except:
            surname = None

        profile_dictionary['last_name'] = surname

        try:
            picture = source.find('img', class_='pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show ember-view')
            avatar = picture['src']
        except:
            avatar = None

        profile_dictionary['avatar'] = avatar

        try:
            linkedin_url = self.profileLink
        except:
            linkedin_url = None

        profile_dictionary['linkedin_url'] = linkedin_url

        try:
            linkedin_username = self.profileLink.rstrip('/')
            linkedin_username = linkedin_username.rsplit('/', 1)[-1]
        except:
            linkedin_username = None

        profile_dictionary['linkedin_username'] = linkedin_username

        try:
            title = name_info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
        except:
            title = None

        profile_dictionary['job_title'] = title

        try:
            location = name_info.find('span' , {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
        except:
            location = None

        profile_dictionary['location_name'] = location

        try:
            about_section = source.find("div", {"id": "about"}).find_parent('section')
            summary = about_section.find_all('span' , {'class': 'visually-hidden'})[1].get_text().strip()
        except:
            summary = 'data not found'

        profile_dictionary['summary'] = summary

        return profile_dictionary
