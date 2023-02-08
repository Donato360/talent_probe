from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ProfileURLs:
    def __init__(self, driver, source):
        self.driver = driver
        self.source = source

    def getProfileURLs(self):
        
        if self.source[0] == 'query':
            self.driver.get('https://www.google.com/')

            accept_google_cookies_button = self.driver.find_element(By.XPATH, '//button/div[contains(text(), "Accept all")]')
            accept_google_cookies_button.click()

            google_search_input = self.driver.find_element(By.XPATH, '//input[@name="q"]')
            google_search_input.send_keys(self.source[1])
            google_search_input.send_keys(Keys.RETURN)

            linkedin_profiles = self.driver.find_elements(By.XPATH, '//div/a[contains(@href,"linkedin.com/in/")]')
            linkedin_profiles = [profile.get_attribute('href') for profile in linkedin_profiles]

            linkedin_profiles = linkedin_profiles + ['https://www.linkedin.com/in/ykpgrr/', 'https://www.linkedin.com/in/lee-braybrooke-73666927/', 'https://www.linkedin.com/in/saman-nejad/', 'https://www.linkedin.com/in/eluert-mukja/', 'https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/', 'https://www.linkedin.com/in/kopanias/']

        if self.source[0] == 'profile':
            linkedin_profiles = [self.source[1]]
            
        if self.source[0] == 'file':
            print(self.source[0])
            print(self.source[1])

        if self.source[0] == 'csv':
            print(self.source[0])
            print(self.source[1])
            pass

        print(linkedin_profiles)
        
        return linkedin_profiles