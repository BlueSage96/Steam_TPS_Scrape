from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import csv

try:      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Optional, recommended for Windows
    options.add_argument('--window-size=1920x1080')  # Optional, set window size

    driver.get("https://store.steampowered.com/category/action_tps")
    title = driver.title # Find the title.
    print(f"Title: {title}")
    
    body = driver.find_element(By.CSS_SELECTOR,'body') 
    
    games = {
        "https://store.steampowered.com/app/1332010/Stray/",
        "https://store.steampowered.com/app/553850/HELLDIVERS_2/"
    }
    
    for get_game in games:
        driver.get(get_game)
        print(driver.title)
            
except Exception as e:
    print(f"An exception occurred: {type(e).__name__}{e}")
finally:
    driver.quit()