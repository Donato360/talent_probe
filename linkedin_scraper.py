# -*- coding: utf-8 -*-

try:
    import time
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import sys
    from selenium_stealth import stealth
    from helpers import average
    from profiles_urls import ProfileURLs
    from profile_general_info import ProfileGeneralInfo
    from profile_education import ProfileEducation
    from profile_experience import ProfileExperience
    from afile import load_cookie

    print('all module are loaded ')
    print()
except Exception as e:
    print('Error ->>>: {} '.format(e))
    print()

def main(source):
    SCROLL_PAUSE_TIME = 1

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        options.add_argument("--headless")
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get('https://www.linkedin.com/login')

        load_cookie(driver, '/tmp/cookie')

        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        print()
        print('Driver: {} has been successfully set'.format(driver.name))
        print()
    except Exception as e:
        print('Webdriver not found')
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()

    try:
        profileUrls_obj = ProfileURLs(driver, source)

        linkedin_profiles = profileUrls_obj.getProfileURLs()

        # linkedin_profiles = linkedin_profiles + ['https://www.linkedin.com/in/ykpgrr/', 'https://www.linkedin.com/in/lee-braybrooke-73666927/', 'https://www.linkedin.com/in/saman-nejad/', 'https://www.linkedin.com/in/eluert-mukja/', 'https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/', 'https://www.linkedin.com/in/kopanias/','https://www.linkedin.com/in/victoriasauven/']

        print('Found profile(s): {}'.format(linkedin_profiles))
        print()
    except Exception as e:
        print('Could not find profiles urls')
        print('Error ->>>: {} '.format(e))
        print()
        sys.exit()   

    current_profile_execution_time = 0
    profiles_execution_times = []

    profiles = []
    x = 1
    
    for profile in linkedin_profiles:
        try:
            profile = profile.replace('uk.linkedin.com', 'www.linkedin.com')
            profile = 'https://www.linkedin.com/in/' + profile

            profileGeneralInfo_obj = ProfileGeneralInfo(driver, profile)
            profileEducation_obj = ProfileEducation(driver, profile)
            profileExperience_obj = ProfileExperience(driver, profile)
    
            start = time.time()

            profile_dict = profileGeneralInfo_obj.getGeneralInfo() | profileEducation_obj.getEducation() | profileExperience_obj.getExperience()
            # sleep(0.1)

            profiles.append(profile_dict)

            end = time.time()

            current_profile_execution_time = (end-start) * 10**3
            profiles_execution_times.append(current_profile_execution_time)

            print('General Information for: {} was processed successfully'.format(profile))
            print()
        except Exception as e:
            print('Could not process profile: {} '.format(profile))
            print('Error ->>>: {} '.format(e))
            print()
            sys.exit()

    average_execution_time = average(profiles_execution_times)
    print("The average time of execution for a profile:", average_execution_time, "ms")
    
    return profiles