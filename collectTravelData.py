from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

import re
import browser
#from urllib.parse import urlparse, urlencode, parse_qs, quote
from urllib.parse import urlparse, urlunparse, urlencode, quote
from datetime import datetime,timedelta
import locale
from bs4 import BeautifulSoup
import time
locale.setlocale(locale.LC_TIME, 'de_DE')
def compareTimes(departureTimeOfTrain1,lastdeparturetime2):    
    
    
    if int(departureTimeOfTrain1[:2]) < int(lastdeparturetime2[:2]):
        input("")
        return False
    else:
        return True

def collect_data(start,destination):
    #expected_title = "Hinfahrt"
    #WebDriverWait(driver, 10).until(EC.title_contains(expected_title))
    
    time.sleep(3)
    


    # Parse the HTML content using Beautiful Soup
    

    stilltrainstofind = True
    lastdeparturetime = None
    date_object = None
    while stilltrainstofind:
        
        i = 0
        o = 0
        soup = BeautifulSoup(browser.driver.page_source, 'html.parser')
        zuege = soup.find_all('div', class_='dauer-umstieg reiseplan__dauer-umstieg')
        price_elements = soup.find_all('div', class_='reise-preis__info-preis')
        zugnummern = soup.find_all('span', class_='verbindungsabschnitt__verkehrsmittel-text')
        while i < len(zuege):
            try: 

                zug = browser.driver.find_element(By.XPATH, f"(//span[@class='dauer-umstieg__dauer'])[{i+1}]")
                parent_element = zug.find_element(By.XPATH, "./ancestor::div[@class='reiseloesung__item']")
                                
                timings = parent_element.find_element(By.XPATH,".//div[contains(@class, 'reiseplan__uebersicht-uhrzeit-von')]")
                departureTimeOfTrain = str(timings.find_element(By.CSS_SELECTOR, '.reiseplan__uebersicht-uhrzeit-sollzeit').text)
                timingsNach = parent_element.find_element(By.XPATH,".//div[contains(@class, 'reiseplan__uebersicht-uhrzeit-nach')]")
                arrivalTimeOfTrain = str(timingsNach.find_element(By.CSS_SELECTOR, '.reiseplan__uebersicht-uhrzeit-sollzeit').text)

                try:
                    test = parent_element.find_element(By.XPATH, '..')
                    precedingCheckNewDateElement = str(test.find_element(By.XPATH, "preceding-sibling::div").text)
                    timor = precedingCheckNewDateElement + " " +  departureTimeOfTrain
                    date_object_departure = datetime.strptime(timor, '%a. %d. %b. %Y %H:%M')

                    if int(departureTimeOfTrain[:2]) > int(arrivalTimeOfTrain[:2]):
                        temptime = browser.departureDate + timedelta(days=1)
                    else:
                        temptime = browser.departureDate

                    time_object_arrival = datetime.strptime(arrivalTimeOfTrain, '%H:%M').time()
                    date_object_arrival = datetime.combine(temptime.date(), time_object_arrival)

                except NoSuchElementException:
                    
                    time_object_departure = datetime.strptime(departureTimeOfTrain, '%H:%M').time()
                    date_object_departure = datetime.combine(browser.departureDate.date(), time_object_departure)
                    
                    if int(departureTimeOfTrain[:2]) > int(arrivalTimeOfTrain[:2]):
                        temptime = browser.departureDate + timedelta(days=1)
                    else:
                        temptime = browser.departureDate
                    time_object_arrival = datetime.strptime(arrivalTimeOfTrain, '%H:%M').time()
                    date_object_arrival = datetime.combine(temptime.date(), time_object_arrival)
                
                if date_object_arrival < date_object_departure:
                    date_object_arrival += timedelta(days=1)

                zugNummer = zugnummern[i].get_text(strip=True)
                try:
                    connectionPrice = parent_element.find_element(By.XPATH, ".//span[@class='reise-preis__preis']").text.replace("€","").rstrip()
                    #connectionPrice = price_elements[i].find('span', class_='reise-preis__preis').get_text(strip=True).replace("€","").rstrip()
                except Exception as e:
                    connectionPrice = "N/A"
                
                #check if the train is already in the datasheet
                if browser.finalDatasheet.get(f"{start} - {destination} | {departureTimeOfTrain} - {arrivalTimeOfTrain}") == None:
                    browser.finalDatasheet[f"{start} - {destination} | {departureTimeOfTrain} - {arrivalTimeOfTrain}"] = {"Preis":connectionPrice,"Zug":zugNummer,"Start":start,"Ziel":destination,"Abfahrt":date_object_departure,"Ankunft":date_object_arrival,"URL":generateURL(departureTimeOfTrain),"Dauer":(date_object_arrival-date_object_departure).total_seconds()/60 }
                    
                    #ankunftszeit und abfahrtszeit müssen alle Datetime Objects sein. Man.
                    lastdeparturetime = departureTimeOfTrain
                else:
                    o += 1
            except StaleElementReferenceException:
                time.sleep(2)
                input("Press enter and see if the issue persists.")
                i-=1
            i+=1

        if o == i:
            break
        
        #spaeterbutton = WebDriverWait(browser.driver, 10).until(EC.element_to_be_clickable((By.XPATH,".//button[contains(@class, 'db-web-button test-db-web-button db-web-button--type-text db-web-button--size-regular db-web-button--type-plain reiseloesung-list-page__spaetere-verbindungen')]")))
        #lastDeparture = list(browser.finalDatasheet)[-1]
        #print("Last Departure Log:",)
        #print("Last Departure Dict:",str(browser.finalDatasheet[lastDeparture].get("Abfahrt")),"\n")
        newSite = generateURL(lastdeparturetime)
        
        browser.driver.get(newSite)
        
        #spaeterbutton.click()

        time.sleep(2)

    time.sleep(2)


    #print(browser.finalDatasheet)
def generateURL(time):

    # Assume browser.driver.current_url is the original URL
    original_url = browser.driver.current_url

    # Extract the fragment part from the URL
    url_parts = original_url.split('hd=')

    base_url = url_parts[0]
    fragment = url_parts[1]
    
    oldDatelength=len("2024-03-05T00:01:30")
    oldDate = fragment[:oldDatelength]
    # Modify the 'hd' parameter directly in the fragment
    modified_fragment = fragment.replace(oldDate, f'{browser.departureDate.strftime("%Y-%m-%d")}T{time}:00')

    # Rebuild the URL with the modified fragment
    modified_url = f"{base_url}hd={modified_fragment}"
    
    return modified_url



# def generateURL(time):
#     # Parse the URL
#     parsed_url = urlparse(browser.driver.current_url)

#     # Parse the fragment into a dictionary
#     query_dict = {k: v[0] for k, v in (param.split('=') for param in parsed_url.fragment.split('&'))}

#     # Modify the timestamp value without additional percent encoding
#     modified_timestamp = f'{browser.departureDate.strftime("%Y-%m-%d")}T00:{time}'
#     print("Query before entering",query_dict['hd'])
#     query_dict['hd'] = modified_timestamp
#     print("Query after entering",query_dict['hd'],"\n")
#     # Encode the modified query parameters
#     encoded_query = '&'.join([f'{key}={quote(value)}' for key, value in query_dict.items()])

#     # Rebuild the URL with the modified query parameters
#     modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, encoded_query, parsed_url.fragment))
#     return modified_url

