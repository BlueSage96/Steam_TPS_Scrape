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
def alpha_games(cursor):
    cursor.execute("""
        SELECT Title
        FROM games
        ORDER BY Title
    """)
    return cursor.fetchall()
print("1. Alphabetical game titles:\n")
q1 = alpha_games(cursor)

for row in q1:
    print(row)
    
#2. Show all Free To Play games.
def free_2_play(cursor):
    cursor.execute("""
        SELECT Title, Original_Prices
        FROM games 
        WHERE Original_Prices = "Free To Play"
        OR Sale_Prices = "Free To Play"                          
    """)
    return cursor.fetchall();

print("\n2. All Free To Play games:\n")
q2 = free_2_play(cursor)

for row in q2:
    print(row)
 
 # 3. Show all games with discounts  
def discounted_games(cursor):
    cursor.execute("""
        SELECT Title, Discounts
        FROM games  
        WHERE Discounts != "0%"                    
    """)
    return cursor.fetchall();
print("\n3. All discounts:\n")
q3 = discounted_games(cursor)

for row in q3:
    print(row)
    
# 4. Find the average user reviews of paid games 
# HAVING average User_Reviews
def average_reviews(cursor):
    cursor.execute("""
     SELECT AVG(User_Reviews), User_Score
     FROM reviews
     JOIN games
     ON games.AppID = reviews.AppID
     WHERE Original_Prices != "Free To Play"
     GROUP BY User_Score
     HAVING AVG(User_Reviews)
""")
    return cursor.fetchall()
print("\n4. Average user reviews of paid games:\n")
q4 = average_reviews(cursor)

for row in q4:
    print(row)
    
#5. Most-Reviewed Discounted Game
def discounted_game(cursor):
    cursor.execute("""
     SELECT Title, Discounts, User_Reviews
     FROM reviews
     JOIN games 
     ON games.AppID = reviews.AppID
     WHERE Discounts != "0%"
     ORDER BY User_Reviews DESC
     LIMIT 1
""")
    return cursor.fetchone()

print("\n5. Most reviewed discounted game:\n")

q5 = discounted_game(cursor)
for row in q5:
    print(row)
    
# Top 5 most-reviewed games
def top_5(cursor): 
    cursor.execute("""
     SELECT Title, User_Reviews, User_Score
     FROM reviews
     JOIN games
     ON games.AppID = reviews.AppID
     ORDER BY User_Reviews DESC
     LIMIT 5               
""")
    return cursor.fetchall()
print("\n6. Top 5 most reviewed games:\n")
q6 = top_5(cursor)
for row in q6:
    print(row)
    
conn.close()