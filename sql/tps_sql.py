import sqlite3
import pandas as pd

# use conn & sqlite3 to create database
conn = sqlite3.connect("tps.db")
#use pd.read_csv
game_tps = pd.read_csv("../web_scrape/clean_games.csv")
print(game_tps)
#csv names.to_sql() --> look up params

#print tables to confirm existence --> 
# variable = pd.read_sql then print(variable)

#close sql database