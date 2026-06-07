#Pandas clean info
import pandas as pd

data_tps = pd.read_csv("steam_deck.csv")
print(f"Original data:\n {data_tps}") #Vanilla data

data_tps = data_tps.rename(columns={"ReviewUrl":"Review URL", "Count":"User Reviews", "Score":"User Score"})
print(f"Changed column names:\n {data_tps}")

data_tps["User Reviews"] = (
    data_tps["User Reviews"]
    .astype(str)
    .str.replace("User Reviews", "", regex=False)
    .str.strip()
)
print(f"Integer for reviews: {data_tps["User Reviews"]}")