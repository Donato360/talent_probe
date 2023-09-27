from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle
import os

# Load connection details from previously saved file
def load_connection_details():
    try:
        with open('connection_details.pickle', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

# Save connection details to a file for future use
def save_connection_details(connection):
    with open('connection_details.pickle', 'wb') as file:
        pickle.dump(connection, file)

# Initialize the driver with headless option and keep it running
def initialize_driver(headless=True):
    # Get the current working directory
    cwd = os.getcwd()  
    # Set the ChromeDriver executable path
    driver_path = os.path.join(cwd, "chromedriver-linux64/chromedriver") 
    service = Service(executable_path=driver_path)
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    # Use ChromeDriver Manager to automatically download and manage the appropriate version of ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Connect to Google, search and parse the results
def connect_to_google_and_search(driver, query):
    # Query to obtain links
    query = 'comprehensive guide to web scraping in python'
    links = [] # Initiate empty list to capture final results
    # Specify number of pages on google search, each page contains 10 #links
    n_pages = 20 
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # soup = BeautifulSoup(r.text, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            links.append(h.a.get('href'))

        print(links)

# Main function to handle script execution
def main(headless=True):
    connection_details = load_connection_details()
    chrome_options = Options()
    if connection_details is not None:
        if headless:
            chrome_options.add_argument("--headless")
            driver = webdriver.Remote(command_executor=connection_details['executor_url'], options=chrome_options)
    else:
        driver = initialize_driver(headless=True)
    
    query = "angular and django jobs in London"
    connect_to_google_and_search(driver, query)
  
    # Save connection details for future use
    connection_details = {
        'executor_url': driver.command_executor._url,
        'capabilities': driver.capabilities
    }
    save_connection_details(connection_details)

# Call the main function to execute the script
if __name__ == "__main__":
    main()