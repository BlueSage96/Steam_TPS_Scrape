#Pandas clean info
import pandas as pd

data_tps = pd.read_csv("steam_deck.csv")
print(f"Original data:\n {data_tps}") #Vanilla data

#Rename some columns
data_tps = data_tps.rename(columns={"ReviewUrl":"Review URL", "Count":"User Reviews", "Score":"User Score","Prices":"Original Prices"})
print(f"Changed column names:\n {data_tps}")

#Convert user reviews from strings to integers
data_tps["User Reviews"] = (
    data_tps["User Reviews"]
    .astype(str)
    .str.replace("User Reviews", "", regex=False)
    .str.strip()
)
print(f"Integer for reviews:\n {data_tps}")

#Split "Original Prices" into a Series of lists
split_prices = data_tps['Original Prices'].str.replace('\n', ' | ')
split_prices = split_prices.str.split(' | ',regex=False)
print(split_prices)

#Parse out discounts and sales prices
data_tps["Original Prices"] = split_prices.apply(lambda x: x[1] if len(x) == 3 else ("0" if "Free" in x else x[0]))
print(f"Original Prices:\n {data_tps["Original Prices"]}")

#Create "Discounts" column
data_tps["Discounts"] = split_prices.apply(lambda x: x[0] if len(x) == 3 else "0%")
print(f"Discounts:\n {data_tps["Discounts"]}")

