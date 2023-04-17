from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login:
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def doLogin(self):
        self.driver.get(self.url)
        #wait for username and password fields to be available
        wait = WebDriverWait(self.driver, 10)
        loginbutton = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/main/div[3]/div[1]/form/div[3]/button')))

        eml = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        eml.send_keys(self.username)
        passwd = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        passwd.send_keys(self.password)
        loginbutton.click()