from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException,
)

from exception import SeleniumBotException
import sys
from logger import logging


class SelectFilters:

    def filters_selection(driver, button):

        try:
            jobs_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//button[normalize-space()='{button}']")))
            jobs_button.click()
            logging.info(f"{button} filter applied...")

        except (
                TimeoutException,
                NoSuchElementException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
                StaleElementReferenceException,
                WebDriverException,
            ) as e:
            logging.error(f"Selenium error while searching: {e.__class__.__name__} - {e}")
            raise SeleniumBotException(e, sys)

        except Exception as e:
            logging.error(f"Failed to navigate to URL: {e}")
            raise SeleniumBotException(e, sys)