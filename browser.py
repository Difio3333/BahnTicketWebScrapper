from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

# Create ChromeOptions instance
chrome_options = webdriver.ChromeOptions()

# Create a dictionary of user profile preferences
user_profile_preferences = {
    "profile.default_content_setting_values.cookies": 2,
    # Add other preferences if needed
}

# Add user profile preferences to ChromeOptions
for key, value in user_profile_preferences.items():
    chrome_options.add_argument(f"--user-data-dir={key}={value}")

# Initialize ChromeDriver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

departureDate = datetime.today()
departureTime = None
departureTrain = None

soup = None
start = None
destination = None
allStops = {}
connectionDictionary = {}
finalDatasheet = {}