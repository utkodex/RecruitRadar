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

import pickle
import os
import time

from exception import SeleniumBotException
import sys
from logger import logging

class link_runner:
    def get_url(driver, url):
        try:
            driver.get(url)
            logging.info(f"Navigated to URL: {url}")
        except Exception as e:
            logging.error(f"Failed to navigate to URL: {e}")
            raise SeleniumBotException(e, sys)
        
class CookieLogin:

    def __init__(self, driver, username, password):
        self.driver = driver
        self.url = "https://www.linkedin.com/feed/"
        self.username = username
        self.password = password
        self.cookie_file = f"cookies_folder\{self.username}_cookies.pkl"
        self.platform_login()


    """Function to save cookies to a file"""
    def save_cookies(self, driver, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(driver.get_cookies(), file)

    """Function to load cookies from a file"""
    def load_cookies(self, driver, file_path):
        try:
            with open(file_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading cookies: {e}. Deleting corrupted file.")
            os.remove(file_path) 

    def platform_login(self):
        try:
            # Navigate to LinkedIn
            link_runner.get_url(self.driver, self.url)
            time.sleep(5)  # Wait for page to load

            # Check if cookies exist
            try:
                self.load_cookies(self.driver, self.cookie_file)
                logging.info("Cookies loaded successfully.")
                self.driver.refresh()  # Refresh to apply cookies

            except FileNotFoundError:
                logging.info("Cookies not found. Logging in manually.")

                enter_username = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//input[@id='username']")))
                enter_username.send_keys(self.username)
                
                enter_password = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//input[@id='password']")))
                enter_password.send_keys(self.password)
                
                enter_password.send_keys(Keys.RETURN)
                time.sleep(10)  # Wait for login to complete

                # Save cookies after successful login
                self.save_cookies(self.driver, self.cookie_file)
                logging.info("Cookies saved successfully.")

        finally:
            logging.info(f"Logged in to {self.url}.")

