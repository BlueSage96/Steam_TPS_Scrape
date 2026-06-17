import streamlit as st  
import pandas as pd     # Used to work with tabular data
import numpy as np      # Helps generate random numbers

import plotly.express as px  # For interactive charts
import sqlite3
from tps_sql import alpha_games, free_2_play, discounted_games, average_reviews, discounted_game, top_5

games_df = pd.read_csv("../web_scrape/clean_games.csv")
reviews_df = pd.read_csv("../web_scrape/clean_reviews.csv")

conn = sqlite3.connect("tps.db")
cursor = conn.cursor()

df1 = alpha_games(cursor)
df2 = free_2_play(cursor)
df3 = discounted_games(cursor)
df4 = average_reviews(cursor)
df5 = discounted_game(cursor)
df6 = top_5(cursor)

# Query 1: Game titles - dropdown list
#convert game titles from tuples to lists
game_titles = [row[0] for row in df1]


#Game title sidebar
with st.sidebar:
    selected_game = st.selectbox(
    "View games",options=game_titles,index=None,placeholder="Select a game"
    )
    st.space("small")
    #show what was selected
    if selected_game:
        st.write(f"Current game: {selected_game}")
        
        df1 = pd.DataFrame(df1,columns=["Title"])
        df1 = df1[df1['Title'] == selected_game]  # Filter the DataFrame based on the selected game
        df2 = pd.DataFrame(df2,columns=["Title", "Discounts"])
        df2 = df2[df2['Title'] == selected_game]  # Filter the DataFrame based on the selected game
        
    else:
        st.info("Select a game from the sidebar.")
        st.stop()
       
    st.space("small")
    radio = st.radio("View Reviews", options=["Very Positive",'Mostly Positive','Mixed','Mostly Negative','Very Negative'])
    filtered_reviews = reviews_df[reviews_df["User_Score"] == radio]
    
    st.space("small")
    #Price slider
    games_df["Original_Prices"] = (
    games_df["Original_Prices"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .replace("Free To Play", 0)
    .astype(float)
    )
    
    games_df["Sale_Prices"] = (
    games_df["Sale_Prices"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .replace("Free To Play", 0)
    .astype(float)
    )
    
    max_price = st.slider(
    "Maximum Price",
    min_value=0,
    max_value=100,
    value=70
    )
    
    filtered_games = games_df[
    games_df["Original_Prices"] <= max_price]
    
    min_reviews = st.slider(
    "Minimum Reviews",
    min_value=0,
    max_value=700000,
    value=50000
)

filtered_reviews = reviews_df[
    reviews_df["User_Reviews"] >= min_reviews
]

#Tabs
tab1, tab2 = st.tabs(["Games","Reviews"])

with tab1:
    st.dataframe(filtered_games)
with tab2:
    st.dataframe(filtered_reviews)
    
    
#Query 2: Free to play games - table
st.subheader('All Free to Play Games')
st.table(df2)

#Query 3: All games with discounts - bar chart
df3 = pd.DataFrame(df3, columns=["Title","Discounts"])
#Convert negative numbers to positives
df3["Discounts"] = (
    df3["Discounts"]
    .astype(str)
    .str.replace("-", "", regex=False)
    .str.strip()
)
st.subheader('All Games with Discounts %')  # Subheading for the chart
bar_chart = px.bar(df3, x='Discounts', y="Title", barmode='group')  # Grouped bar chart
st.plotly_chart(bar_chart)

#Query 4 - Average user reviews of paid games - pie chart
df4 = pd.DataFrame(df4,columns=["User_Reviews","User_Score"])
pie_chart = px.pie(df4,names="User_Score",
values="User_Reviews",title="Average Reviews by User Score")
st.plotly_chart(pie_chart)

#Query 5 - most reviwed-discounted game - metric
title = df5[0]
discount = df5[1]
reviews = df5[2]

st.metric(
    label="Most Reviewed Discounted Game",
    value=title,
)

st.metric(
    label="Review Count",
    value=reviews
)

#Query 6 - Top 5 most-reviews games
st.subheader("Top 5 Most Reviewed Games")
df6 = pd.DataFrame(df6, columns=["Title","User_Reviews","User_Score"])
bar_chart = st.bar_chart(df6,x="User_Score",y="User_Reviews",horizontal=True)