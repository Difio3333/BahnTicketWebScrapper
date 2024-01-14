from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import browser

from bs4 import BeautifulSoup
import time

def convert_to_minutes(duration):
    hours, minutes = 0, 0
    match = re.match(r'(\d+)h(?:\s*(\d*)min)?', duration)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes


def find_quickest_connection():
    #expected_title = "Hinfahrt"
    #WebDriverWait(driver, 10).until(EC.title_contains(expected_title))
    
    time.sleep(5)
    page_source = browser.driver.page_source


    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    zuege = soup.find_all('div', class_='dauer-umstieg reiseplan__dauer-umstieg')

    durations_in_minutes = []
    for element in zuege:
        
        fahrtdurationSpan = element.find('span', class_='dauer-umstieg__dauer')

        fahrtduration = fahrtdurationSpan.get_text(strip=True) if fahrtdurationSpan else None
        durations_in_minutes.append(convert_to_minutes(fahrtduration))
        
        
    minDurationIndex = durations_in_minutes.index(min(durations_in_minutes))

    lowest_price_element = browser.driver.find_element(By.XPATH, f"(//span[@class='dauer-umstieg__dauer'])[{minDurationIndex+1}]")

    # 2. Navigate to the parent element to find the Weiter button
    parent_element = lowest_price_element.find_element(By.XPATH, "./ancestor::div[@class='reiseloesung__item']")
    
    
    # 3. Find and click the "Details" button
    detail_button = parent_element.find_element(By.XPATH, ".//button[contains(@class, 'db-web-button test-db-web-button db-web-button--type-text db-web-button--size-regularResponsive db-web-button--type-plain db-web-expansion-toggle__button')]")
    detail_button.click()
    time.sleep(2)
    halte_button = parent_element.find_element(By.XPATH, ".//button[contains(@class, 'db-web-button test-db-web-button db-web-button--type-text db-web-button--size-regular db-web-button--type-plain db-web-expansion-toggle__button')]")
    halte_button.click()

    timings = parent_element.find_element(By.XPATH,".//div[contains(@class, 'reiseplan__uebersicht-uhrzeit-von')]")
    departureTimeOfQuickestTrain = timings.find_element(By.CSS_SELECTOR, '.reiseplan__uebersicht-uhrzeit-sollzeit')
    browser.departureTime = departureTimeOfQuickestTrain.text

    allDepartureTimes = soup.find_all("div",class_="reiseplan__uebersicht-uhrzeit-von")
    #print(allDepartureTimes[0].find('time',class_='reiseplan__uebersicht-uhrzeit-sollzeit').get_text(strip=True))

    #this resouping is important because new info is on the card.
    soup = BeautifulSoup(browser.driver.page_source, 'html.parser')
    
    stop_name_elements= soup.find_all("div",class_="verbindungs-zwischenhalt__name test-zwischenhalt-name")
    stop_time_elements = soup.find_all("time",class_="zeit-anzeige__sollzeit")
    stop_time_elements = stop_time_elements[0::2]
    tempDict = {}
    for stop_name_element, stop_time_element in zip(stop_name_elements, stop_time_elements):
        stop_name = stop_name_element.get_text(strip=True)
        stop_time = stop_time_element.get_text(strip=True)
        
        # Check if the "Hält nur zum Aussteigen" text is present in the stop description
        meldungen_element = stop_name_element.find_next("div", class_="verbindungs-zwischenhalt__meldungen")
        meldung_text_element = meldungen_element.find("span", class_="priorisierte-meldung__text")

        # If the text is not present, add the stop to the list
        if meldung_text_element is None or "Hält nur zum Aussteigen" not in meldung_text_element.get_text(strip=True):
            tempDict[stop_name] = {"Departure Time": stop_time}
            

    browser.departureTrain = parent_element.find_element(By.CLASS_NAME, "verbindungsabschnitt__verkehrsmittel-text").text
    
    return tempDict


    
