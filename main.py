import browser
import mainconnectionsearch
import schnellsteverbindungfinden
import collectTravelData
import convertToExcel
from datetime import datetime

current_datetime = datetime.now()


#Edit these for variables to your desired start, destination, departure date as well as departure time. 
browser.start = "München"
browser.destination = "Berlin"

#This is YYYY.MM.DD or YYYY.M.D depending if your month or day are single digit or not.
browser.departureDate = datetime(2024,2,15)
browser.departureTime = "00:01"


#leave this as is
stunde = browser.departureTime[:2]
minute = browser.departureTime[3:5]


mainconnectionsearch.enter_route(browser.start,browser.destination,timing=True,abfahrtsdatum=browser.departureDate,stunde=stunde,minute=minute,direktVerbindung=False)
collectTravelData.collect_data(browser.start,browser.destination)


#Type in your checkpoints manually in the list or check the comment below.
browser.allStops = ["Nürnberg"]

#You can also let the webscrapper find the checkpoints by removing the # from the line below but this might find tons of them and take a longer time.
#browser.allStops = schnellsteverbindungfinden.find_quickest_connection()


for connection in browser.allStops:

    mainconnectionsearch.enter_route(browser.start,connection,timing=True,abfahrtsdatum=browser.departureDate,stunde=stunde,minute=minute)
    
    collectTravelData.collect_data(browser.start,connection)
    
    mainconnectionsearch.enter_route(connection,browser.destination,timing=True,abfahrtsdatum=browser.departureDate,stunde=stunde,minute=minute)
    collectTravelData.collect_data(connection,browser.destination)
    

convertToExcel.converting_excel(browser.finalDatasheet)