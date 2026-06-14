import sqlite3
import pandas as pd

# use conn & sqlite3 to create database
conn = sqlite3.connect("tps.db")
cursor = conn.cursor()

#use pd.read_csv
games_df = pd.read_csv("../web_scrape/clean_games.csv")
# print(f"Game csv loaded:\n {games_df}")

reviews_df = pd.read_csv("../web_scrape/clean_reviews.csv")
# print(f"Review csv loaded:\n {reviews_df}")

# Create or replace tables
games_df.to_sql("games",conn,if_exists="replace",index=False)
reviews_df.to_sql("reviews",conn,if_exists="replace",index=False)

#queries

# 1. List all games alphabetically.
q1 = cursor.execute("""
    SELECT Title 
    FROM games 
    ORDER BY Title
""")

print("Alphabetical game titles:\n")
for row in q1:
    print(row)
    
#2. Show all Free To Play games.
q2 = cursor.execute("""
    SELECT Original_Prices as op, Sale_Prices as sp
	FROM games 
	WHERE Original_Prices = "Free To Play"
    OR Sale_Prices = "Free To Play"                          
""")

print("All Free To Play games:\n")
for row in q2:
    print(row)
 
 # 3. Show all games with discounts   
q3 = cursor.execute("""
    SELECT Title, Discounts
	FROM games  
    WHERE Discounts != "0%"                    
""")

print("All discounts:\n")
for row in q3:
    print(row)
    
     
conn.close()