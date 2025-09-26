from run_browser import run_browser
# from run_browser import 
from run_browser.link_runner import link_runner, CookieLogin
from src import search, filters_selection
from src.filters_selection import SelectFilters
import time

print("started...")
rb = run_browser()

driver = rb.driver
username = "utkarsh.s@lawsikho.in"
password = "Team123#"
keywords = "Mindrift"

CookieLogin(driver, username, password)

s = search.LinkedinSearch(driver, keywords)
s.searching()
time.sleep(2)

button = "Companies"
SelectFilters.filters_selection(driver, button)

time.sleep(10)

