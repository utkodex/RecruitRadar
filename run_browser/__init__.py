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


from config.config_loader import load_config
from exception import SeleniumBotException
import sys
import yaml
from logger import logging

class run_browser:
    def __init__(self, headless=True):
        load_dotenv()
        self.headless = headless
        self.config=load_config()
        self.brower_init() 

    def brower_init(self):
        try:
            # Create a fake user-agent
            ua = UserAgent()
            fake_user_agent = ua.random 

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
            self.driver = uc.Chrome(version_main=self.config["chrome-driver-version"], options=options)
            return self.driver
        except yaml.YAMLError as e:
            logging.error('YAML error: %s', e)
            raise SeleniumBotException(e, sys)
        except Exception as e:
            logging.error(f"Error initializing browser: {e}")
            raise SeleniumBotException(e, sys)
    
if __name__ == "__main__":
    rb = run_browser()
    driver = rb.driver
    # time.sleep(10)