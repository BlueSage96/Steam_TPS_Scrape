import streamlit as st  
import pandas as pd     # Used to work with tabular data
import numpy as np      # Helps generate random numbers

import plotly.express as px  # For interactive charts
import sqlite3
from tps_sql import alpha_games

games_df = pd.read_csv("../web_scrape/clean_games.csv")
reviews_df = pd.read_csv("../web_scrape/clean_reviews.csv")

conn = sqlite3.connect("tps.db")
cursor = conn.cursor()
df1 = alpha_games(cursor)

#convert game titles from tuples to lists
game_titles = [row[0] for row in df1]


#Game title sidebar
with st.sidebar:
    selected_game = st.selectbox(
    "View games",options=game_titles,index=None,placeholder="Select a game"
    )
    
#Tabs
tab1, tab2 = st.tabs(["Games","Reviews"])

with tab1:
    st.dataframe(games_df)
with tab2:
    st.dataframe(reviews_df)