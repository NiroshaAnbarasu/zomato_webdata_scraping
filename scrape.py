import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.binary_location = "/home/nandakumar/miniconda3/envs/selenium_corp/bin/firefox"
service = Service()

driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 25)

url = "https://www.zomato.com/chennai/macaw-by-stories-sholinganallur"
driver.get(url)

def safe_get(xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
# Name
name = safe_get('//h1')

# Timing
def get_timing():
    possible_xpaths = [
        '//p[contains(text(),"AM") or contains(text(),"PM") or contains(text(),"noon")]',
        '//span[contains(text(),"AM") or contains(text(),"PM") or contains(text(),"noon")]',
        '//div[contains(text(),"AM") or contains(text(),"PM") or contains(text(),"noon")]'
    ]

    for xp in possible_xpaths:
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
            timing_text = element.text.strip()
            if "–" in timing_text:   # ensure it's a time range
                return timing_text
        except:
            continue

    return "Not Found"


timing = get_timing()

# Dining and Rating
import re

def get_ratings():
    try:
        rating_elements = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, '//div[contains(@class,"cILgox")]'
        )))
        ratings = []
        for el in rating_elements[:2]:  # first two ratings
            match = re.search(r'\d+(\.\d+)?', el.text.strip())
            ratings.append(match.group(0) if match else el.text.strip())
        # Assign
        dining = ratings[0] if len(ratings) > 0 else "Not Found"
        delivery = ratings[1] if len(ratings) > 1 else "Not Found"
        return dining, delivery
    except:
        return "Not Found", "Not Found"

dining_rating, delivery_rating = get_ratings()

# Address
def get_address():
    xpaths = [
        '//p[contains(@class,"sc-clNaTc")]',         # Most common
        '//div[contains(@class,"sc-1hez2tp-0")]',   # Sometimes used
        '//p[contains(text(),"Chennai")]',          # Fallback if city is shown
    ]
    for xp in xpaths:
        try:
            return safe_get(xp)
        except:
            continue
    return "Not Found"

address = get_address()

# Cuisine
try:
    cuisines_elements = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//a[contains(@href,"/restaurants/") and not(contains(@href,"reviews"))]')
    ))
    cuisines_list = [c.text.strip() for c in cuisines_elements if c.text.strip()]
    cuisines = ", ".join(dict.fromkeys(cuisines_list))
except:
    cuisines = "Not Found"

# Price
def get_price():
    xpaths = [
        '//p[contains(text(),"for two")]',      # common layout
        '//p[contains(text(),"for one")]',      # fallback (some cafes show for one)
    ]
    for xp in xpaths:
        try:
            return safe_get(xp)
        except:
            continue
    return "Not Found"

price = get_price()

# Phone number
def get_phone_number():
    xpaths = [
        '//a[starts-with(@href,"tel:")]',   # standard tel link
        '//p[contains(text(),"+91")]',      # fallback if number in paragraph
    ]
    for xp in xpaths:
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
            phone = element.text.strip()
            return phone
        except:
            continue
    return "Not Found"

phone_number = get_phone_number()

data = {
    "Name": [name],
    "Address": [address],
    "Cuisines": [cuisines],
    "Timing": [timing],
    "Phone Number": [phone_number],
    "Price": [price],
    "Dining Rating": [dining_rating],
    "Delivery Rating": [delivery_rating],
}

df = pd.DataFrame(data)
df.to_excel("zomato_data.xlsx", index=False)

print("Data extracted successfully and saved to zomato_data.xlsx")

driver.quit()
