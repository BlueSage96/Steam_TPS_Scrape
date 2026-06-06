#Scrape raw data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import json
import csv
import time

try:      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Optional, recommended for Windows
    options.add_argument('--window-size=1920x1080')  # Optional, set window size
    # driver = webdriver.Chrome()
    driver.get("https://store.steampowered.com/category/action_tps")
    
    # Wait for game cards to load
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/app/']")))

    title = driver.title 
    print(f"Title: {title}")
    
    body = driver.find_element(By.CSS_SELECTOR,'body') 
    time.sleep(5)
    
    cards = driver.find_elements(By.CLASS_NAME, "ImpressionTrackedElement")
    #Find reviews separately
    reviews = driver.find_elements(By.CSS_SELECTOR, "a[href*='#app_reviews_hash']")
 
    #sets --> handle duplicates
    handle_duplicates = set()
    
    card_dict = []
    review_dict = []
    
    for get_card in cards:
        # skip links that don't have an image
        if not get_card.find_element(By.TAG_NAME, "img"):
         continue
     
        image = get_card.find_element(By.TAG_NAME,"img")
        title = image.get_attribute("alt")
        
        #handle urls
        links = get_card.find_element(By.TAG_NAME,"a")
        url = links.get_attribute("href")
        
        if not url:
            continue
        
        #Normalizing urls
        url = url.split("?")[0]      # remove ?snr=
        url = url.rstrip("/")        # remove trailing /
        
        if url in handle_duplicates:
            continue
        
        handle_duplicates.add(url)
        
        #Price
        price = get_card.find_element(By.CLASS_NAME,"StoreSalePriceWidgetContainer")
        
        card_dict.append({
            "Title": title,
            "Url": url,
            "Image": image.get_attribute("src"),         
            "Prices" : price.text
        })
        
    # print(f"Dictionary: {card_dict}")
    card_frame = pd.DataFrame(card_dict)
    # print(card_frame)
    
    #Reviews - get scores
    for views in reviews:
        #extract review scores
        scores = views.find_elements(By.TAG_NAME, "div")
        
        #Make variables for review and count
        review_score = ""
        review_count = ""

        for score in scores:
            aria = score.get_attribute("aria-label")
            #If it's not aria, keep going --> like image above
            if not aria:
                continue

            if "review score" in aria.lower():
                review_score = score.text

            elif "user reviews" in aria.lower():
                review_count = aria
    
        # add to dictionary
        review_dict.append({
            "Score": review_score,
            "Count": review_count 
        })
    review_frame = pd.DataFrame(review_dict)
    # print(review_frame)
    #loop through both dictionaires and combine them
    #test both dictionaries before combining!
except Exception as e:
    print(f"An exception occurred: {type(e).__name__}{e}")
finally:
    driver.quit()
    
    