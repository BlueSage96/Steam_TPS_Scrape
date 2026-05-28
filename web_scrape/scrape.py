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

    title = driver.title # Find the title.
    print(f"Title: {title}")
    
    body = driver.find_element(By.CSS_SELECTOR,'body') 
    games = driver.find_elements(By.CSS_SELECTOR, "a[href*='/app/']")
    
    for get_game in games:
        # print(get_game)
        # href for url - get_attribute 
        url = get_game.get_attribute("href")
        # print(url)
        #Conditional to check for "img" --> extract image and then title from the image
        # Use find_element for image
        #handle duplicates
        
        #build a dictionary for: title, publisher, release date, reviews (for analytics)
        game_dict = {
            "Url": url
        }
        print(game_dict)
        
except Exception as e:
    print(f"An exception occurred: {type(e).__name__}{e}")
finally:
    driver.quit()