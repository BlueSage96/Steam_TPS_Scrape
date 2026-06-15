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

print("1. Alphabetical game titles:\n")
for row in q1:
    print(row)
    
#2. Show all Free To Play games.
q2 = cursor.execute("""
    SELECT Title, Original_Prices, Sale_Prices
	FROM games 
	WHERE Original_Prices = "Free To Play"
    OR Sale_Prices = "Free To Play"                          
""")

print("\n2. All Free To Play games:\n")
for row in q2:
    print(row)
 
 # 3. Show all games with discounts  
q3 = cursor.execute("""
    SELECT Title, Discounts
	FROM games  
    WHERE Discounts != "0%"                    
""")

print("\n3. All discounts:\n")
for row in q3:
    print(row)
    
# 4. Find the average user reviews of paid games 
# HAVING average User_Reviews
q4 = cursor.execute("""
     SELECT AVG(User_Reviews), User_Score
     FROM reviews
     JOIN games
     ON games.AppID = reviews.AppID
     WHERE Original_Prices != "Free To Play"
     GROUP BY User_Score
     HAVING AVG(User_Reviews)
""")

print("\n4. Average user reviews of paid games:\n")
for row in q4:
    print(row)
    
#Most-Reviewed Discounted Game
q5 = cursor.execute("""
     SELECT Title, Discounts, User_Reviews
     FROM reviews
     JOIN games 
     ON games.AppID = reviews.AppID
     WHERE Discounts != "0%"
     ORDER BY User_Reviews DESC
     LIMIT 1
""")

print("\n5. Most reviewed discounted game:\n")
for row in q5:
    print(row)
    
# Top 5 most-reviewed games
q6 = cursor.execute("""
     SELECT Title, User_Reviews, User_Score
     FROM reviews
     JOIN games
     ON games.AppID = reviews.AppID
     ORDER BY User_Reviews DESC
     LIMIT 5               
""")

print("\n6. Top 5 most reviewed games:\n")
for row in q6:
    print(row)
    
conn.close()