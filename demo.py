# below code is to check the logging config
# from logger import logging

# logging.debug("This is a debug message.")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")

# --------------------------------------------------------------------------------

# # below code is to check the exception config
# from logger import logging
# from exception import MyException
# import sys

# try:
#     a = 1+'Z'
# except Exception as e:
#     logging.info(e)
#     raise MyException(e, sys) from e

# --------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent
import undetected_chromedriver as uc

import time
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

# Create a fake user-agent
ua = UserAgent()
fake_user_agent = ua.random  # Get a random user-agent

# Set up undetected-chromedriver
options = uc.ChromeOptions()
options.add_argument(f"user-agent={fake_user_agent}") 
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-cache")
options.add_argument("--aggressive-cache-discard")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-offline-load-stale-cache")
options.add_argument("--disk-cache-size=0")
# Uncomment if you want headless mode
# options.add_argument("--headless=new")

# Initialize undetected-chromedriver
driver = uc.Chrome(version_main=139, options=options)



linkedin_username = os.getenv("USERNAME2")
linkedin_password = os.getenv("PASSWORD")

linkedin_url = "https://www.linkedin.com/feed/" 
cookies_file = f"cookies\{linkedin_username}_cookies.pkl"

# Function to save cookies to a file
def save_cookies(driver, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

# Function to load cookies from a file  ``
def load_cookies(driver, file_path):
    try:
        with open(file_path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except (EOFError, pickle.UnpicklingError) as e:
        print(f"Error loading cookies: {e}. Deleting corrupted file.")
        os.remove(file_path)  # Remove the corrupted file

try:
    # Navigate to LinkedIn
    driver.get(linkedin_url)
    time.sleep(5)  # Wait for page to load

    # Check if cookies exist
    try:
        load_cookies(driver, cookies_file)
        print("Cookies loaded successfully.")
        
        driver.refresh()  # Refresh to apply cookies

        # enter_username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//button[@class='member-profile__details']")))
        # enter_username.click()
    except FileNotFoundError:
        print("Cookies not found. Logging in manually.")

        enter_username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//input[@id='username']")))
        enter_username.send_keys(linkedin_username)
        
        enter_password = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//input[@id='password']")))
        enter_password.send_keys(linkedin_password)
        
        enter_password.send_keys(Keys.RETURN)
        time.sleep(10)  # Wait for login to complete

        # Save cookies after successful login
        save_cookies(driver, cookies_file)
        print("Cookies saved successfully.")

finally:
    print("done")

time.sleep(20)  # Wait for 2 seconds to ensure the browser is fully loaded
