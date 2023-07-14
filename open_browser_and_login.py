# -*- coding: utf-8 -*-

try:
    import sys
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium_stealth import stealth
    from login import Login
    from afile import save_cookie
    from contextlib import closing
    from parameters import username, password
    from helpers import logger
except Exception as e:
    logger.error(f'Problems importing libraries. Error: {str(e)}')

def main():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        options.add_argument("--headless")
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        with closing(webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)) as driver:
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )

            login_url = 'https://www.linkedin.com/login'
            login_obj = Login(driver, login_url, username, password)
            login_obj.doLogin()

            save_cookie(driver, '/tmp/cookie')
    except WebDriverException as e:
        logger.error('%s - %s', str(e), sys.exc_info()[2].tb_frame.f_globals['__name__'])
        return

if __name__ == "__main__":
        # Call the main function
        main()