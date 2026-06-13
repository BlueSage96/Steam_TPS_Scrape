import sqlite3
import pandas as pd

# use conn & sqlite3 to create database
conn = sqlite3.connect("tps.db")
#use pd.read_csv
games_df = pd.read_csv("../web_scrape/clean_games.csv")
print(f"Game csv loaded:\n {games_df}")

reviews_df = pd.read_csv("../web_scrape/clean_reviews.csv")
print(f"Review csv loaded:\n {reviews_df}")

# Create or replace tables
games_df.to_sql("games",conn,if_exists="replace",index=False)
reviews_df.to_sql("reviews",conn,if_exists="replace",index=False)

