from time import sleep
from selenium.webdriver.common.by import By

class Login:
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def doLogin(self):
        # self.driver.maximize_window()
        # sleep(0.1)

        self.driver.get(self.url)
        self.driver.implicitly_wait(3)

        eml = self.driver.find_element(by=By.ID, value="username")
        eml.send_keys(self.username)
        passwd = self.driver.find_element(by=By.ID, value="password")
        passwd.send_keys(self.password)
        loginbutton = self.driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
        loginbutton.click()