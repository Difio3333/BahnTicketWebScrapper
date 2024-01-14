from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from browser import *

from bs4 import BeautifulSoup
import time



def go_to_main_page():
    driver.switch_to.new_window('tab')
    # URL of the website you want to scrape
    url = 'https://www.bahn.de'
    # Open the website in the browser
    driver.get(url)

    expected_title = "DB Fahrplan, Auskunft, Tickets, informieren und buchen - Deutsche Bahn"
    WebDriverWait(driver, 10).until(EC.title_contains(expected_title))

def enter_route(start,destination,timing=False,abfahrtsdatum=None,stunde=None,minute=None,direktVerbindung=False):
    go_to_main_page()
    # Wait for the "Von" input field to be clickable
    von_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="quickFinderBasic-von"]'))
    )
    # Type text into the "Von" input field
    von_input.clear()
    von_input.send_keys(start)
    autocomplete_abfahrt = driver.find_element(By.XPATH, '//button[@class="db-web-button test-db-web-button db-web-button--type-primary db-web-button--size-large quick-finder-basic__search-btn quick-finder-basic__search-btn--desktop"]')

    suggestion_list = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'db-web-select-list-item'))
    )


    # Click on the first suggestion in the list
    suggestion_list.click()


    # Wait for the "Nach" input field to be clickable
    nach_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="quickFinderBasic-nach"]'))
    )


    # Type text into the "Nach" input field
    nach_input.clear()
    nach_input.send_keys(destination)

    suggestion_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'db-web-select-list-item'))
    )

    # Click on the first suggestion in the list
    suggestion_list.click()

    if timing:
        zeitauswahl_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.quick-finder-zeitauswahl.quick-finder-options__option.quick-finder-options__hinfahrt'))
        )

        # Click on the "quick-finder-zeitauswahl" element
        zeitauswahl_element.click()
        time.sleep(1)

        date_picker_input = driver.find_element(By.CLASS_NAME, "db-web-date-picker-input__field")

        # Click on the date picker input field to open the calendar
        date_picker_input.click()
        time.sleep(1)
        
        date_picker_input.send_keys(abfahrtsdatum.strftime("%d"))

        #if abfahrtsdatum.strftime("%d")[0] == "0":
        #     date_picker_input.send_keys(Keys.ARROW_RIGHT)

        date_picker_input.send_keys(abfahrtsdatum.strftime("%m"))
        
        if abfahrtsdatum.strftime("%m")[:2] == "01":
            date_picker_input.send_keys(Keys.ARROW_RIGHT)
        
        date_picker_input.send_keys(abfahrtsdatum.strftime("%Y"))
        
        time_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.db-web-time-picker-input__input')))

        time_input.click()
        time.sleep(1)
        time_input.send_keys(stunde)
        time_input.send_keys(minute)
        time.sleep(1)


        uebernehmen_button = driver.find_element(By.CLASS_NAME, "quick-finder-overlay-control-buttons__button--commit")
        uebernehmen_button.click()
    

    if direktVerbindung:
        button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(@class, 'quick-finder-extended-options__switch-item') and contains(., 'Nur Direktverbindungen')]"))
            )
        button.click()
        time.sleep(1)
    
    suchen_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="db-web-button test-db-web-button db-web-button--type-primary db-web-button--size-large quick-finder-basic__search-btn quick-finder-basic__search-btn--desktop"]'))
    )
    

    suchen_button.click()



