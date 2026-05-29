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
    games = driver.find_elements(By.CSS_SELECTOR, "a[href*='/app/']")
    
    #sets --> handle duplicates
    handle_duplicates = set()
    
    game_dict = []
    print("Number of game elements found:", len(games))
    
    for get_game in games:
        # skip links that don't have an image
        if not get_game.find_elements(By.TAG_NAME, "img"):
         continue
     
        image = get_game.find_element(By.TAG_NAME,"img")
        title = image.get_attribute("alt")
        
        #handle urls
        url = get_game.get_attribute("href")
        
        if not url:
            continue
        
        #Normalizing urls
        url = url.split("?")[0]      # remove ?snr=
        url = url.rstrip("/")        # remove trailing /
        
        if url in handle_duplicates:
            continue
        
        handle_duplicates.add(url)

        #build a dictionary for: title, publisher, release date, reviews (for analytics)
        game_dict.append({
            "Title": title,
            "Url": url,
            "Image": image
        })
    print(game_dict)
    game_frame = pd.DataFrame(game_dict)
    # print(game_frame)
        
except Exception as e:
    print(f"An exception occurred: {type(e).__name__}{e}")
finally:
    driver.quit()