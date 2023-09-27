# -*- coding: utf-8 -*-

try:
    import time
    from afile import load_cookie
    import os
    import sys
    from urllib.error import URLError
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium_stealth import stealth
    from helpers import average, logger
    from login import Login
    from contextlib import closing
    from parameters import username, password
    from profiles_urls import ProfileURLs
    from profile_general_info import ProfileGeneralInfo
    from profile_education import ProfileEducation
    from profile_experience import ProfileExperience
    from profile_language import ProfileLanguage
    from profile_certification import ProfileCertification
    from profile_skill import ProfileSkill
    from profile_organisation import ProfileOrganization
    from profile_project import ProfileProject
except ImportError as e:
    logger.error(f'Failed to import module: {str(e)}')
    sys.exit()

def main(source):
    scroll_pause_time = 1

    try:
        # Get the current working directory
        cwd = os.getcwd()  
        # Set the ChromeDriver executable path
        driver_path = os.path.join(cwd, "chromedriver-linux64/chromedriver") 
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        with closing(webdriver.Chrome(service=service, options=options)) as driver:
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
        
    except WebDriverException as e:
        logger.error('Webdriver error:', str(e))
        sys.exit()

    try:
        profileUrls_obj = ProfileURLs(driver, source)

        linkedin_profiles = profileUrls_obj.getProfileURLs()

        # linkedin_profiles = linkedin_profiles + ['https://www.linkedin.com/in/ykpgrr/', 'https://www.linkedin.com/in/lee-braybrooke-73666927/', 'https://www.linkedin.com/in/saman-nejad/', 'https://www.linkedin.com/in/eluert-mukja/', 'https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/', 'https://www.linkedin.com/in/kopanias/','https://www.linkedin.com/in/victoriasauven/']
    except Exception as e:
        logger.error(f'Could not find profiles urls. Error: {str(e)}')
        sys.exit()

    current_profile_execution_time = 0
    profiles_execution_times = []

    profiles = []
    
    for profile in linkedin_profiles:
        try:
            profile = profile.replace('uk.linkedin.com', 'www.linkedin.com')
            profile = 'https://www.linkedin.com/in/' + profile

            profileGeneralInfo_obj = ProfileGeneralInfo(driver, profile)
            profileEducation_obj = ProfileEducation(driver, profile)
            profileExperience_obj = ProfileExperience(driver, profile)
            profileLanguage_obj = ProfileLanguage(driver, profile)
            profileCertification_obj = ProfileCertification(driver, profile)
            profileOrganization_obj = ProfileOrganization(driver,profile)
            profileProject_obj = ProfileProject(driver, profile)
            profileSkill_obj = ProfileSkill(driver, profile)
    
            start = time.time()

            profile_dict = profileGeneralInfo_obj.getGeneralInfo() | profileEducation_obj.getEducation() | profileExperience_obj.getExperience() | profileLanguage_obj.getLanguage() | profileCertification_obj.getCertification() |profileOrganization_obj.getOrganization() | profileProject_obj.getProject() | profileSkill_obj.getSkill()

            profiles.append(profile_dict)

            end = time.time()

            current_profile_execution_time = (end-start) * 10**3
            profiles_execution_times.append(current_profile_execution_time)
        except Exception as e:
            logger.error(f'Could not process profile: {profile}. Error: {str(e)}')
            continue

    average_execution_time = average(profiles_execution_times)
    print("The average time of execution for a profile:", average_execution_time, "ms")
    
    return profiles