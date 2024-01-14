# General Info
This software scrapes bahn.de for ticket prices on a particular day and creates an excel list with all connections, durations and corresponding prices.
The interesting thing is that you can add stops to the scrapper (or the scrapper can find them itself) which may allow you to travel from A to B a bit cheaper than normal.
So a ticket from Munich to Berlin sometimes costs 100€ but tickets from Munich to Leipzig and then from Leipzig to Berlin might only cost 90€ and if you're lucky you'll actually sit in the same train.
This software aims to find these connections.

# Disclaimer
It is against the terms of service to scrape bahn.de and doing it might make them ban you from using bahn.de and all their other services. It is your responsibility to obey their terms of services.
[Read more about it here](https://www.bahn.de/nutzungsbedingungen)


# Dependencies
```bash
pip install selenium
pip install bs4
```

# Manual
1. Open and edit line 12, 13, 16, 17 and line 30 in main.py to set your departure and arrival locations and times.
2. Run main.py
3. On your first run you might have to quickly, manually accept the cookies. It might get stuck once you have done that but if you rerun main.py it'll usually work.
4. Once it has finished you'll get an .xlsx file. There'll be a Original Data sheet and a Connections sheet. The Original Data sheet holds all single connections that have been scraped and the connections sheets has all the possible connections in them.
5. Now you just have to compare the prices and durations and if you found a connection that suits you, just click on the two URLs provided in the right most colums.


# Example
Here is a picture of a couple of connections from Munich to Berlin via Nürnberg.
[Example Sheet](https://github.com/Difio3333/BahnTicketWebScrapper/assets/86922197/76837fa5-ed94-4147-8f16-366da830d9d2)
