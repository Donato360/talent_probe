from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

class Login:
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def doLogin(self):
        self.driver.get(self.url)
        
        wait = WebDriverWait(self.driver, 10)
        login_button = wait.until(element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))

        email_field = self.driver.find_element(By.ID, 'username')
        email_field.send_keys(self.username)
        
        password_field = self.driver.find_element(By.ID, 'password')
        password_field.send_keys(self.password)
        
        login_button.click()
