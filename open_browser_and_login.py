# -*- coding: utf-8 -*-

try:
    from parameters import username, password
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import sys
    from selenium_stealth import stealth
    from login import Login
    from afile import save_cookie
    
    print('all module are loaded ')
    print()
except Exception as e:
    print('Error ->>>: {} '.format(e))
    print()

def main():

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("detach", True)
        options.add_argument("--headless")
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        global driver

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # browser.set_window_size(1800, 900)
        print('Driver: {} has been successfully set'.format(driver.name))
        print()
    except Exception as e:
        print('Webdriver not found')
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()

    try:
        login_url = 'https://www.linkedin.com/login'
        login_obj = Login(driver, login_url, username, password)
        login_obj.doLogin()
        print('Login to: {} was successfull'.format(login_url))
        print()

        print(f'driver.command_executor._url: {driver.command_executor._url}')
        print(f'driver.session_id: {driver.session_id}')

        save_cookie(driver, '/tmp/cookie')

    except Exception as e:
        print('Could not login to {} '.format(login_url))
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()

if __name__ == "__main__":
    main()