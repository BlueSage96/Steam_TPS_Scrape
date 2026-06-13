#Pandas clean info
import pandas as pd

data_tps = pd.read_csv("steam_deck.csv")
print(f"Original data:\n {data_tps}") #Vanilla data

#Rename some columns
data_tps = data_tps.rename(columns={"Url":"URL","ReviewUrl":"Review URL", "Count":"User Reviews", "Score":"User Score","Prices":"Original Prices"})
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
print(f"Split Original Prices:\n {split_prices}")

#Parse out discounts and sales prices
data_tps["Original Prices"] = split_prices.apply(lambda x: x[1] if len(x) == 3 else ("0" if "Free" in x else x[0]))
print(f"Original Prices:\n {data_tps['Original Prices']}")

#Create "Discounts" column
data_tps["Discounts"] = split_prices.apply(lambda x: x[0] if len(x) == 3 else "0%")
print(f"Discounts:\n {data_tps['Discounts']}")

#Sale Prices
data_tps["Sale Prices"] = split_prices.apply(lambda x: x[2] if len(x) == 3 else ("0" if "Free" in x else x[0]))
print(f"Sale Prices:\n {data_tps['Sale Prices']}")

print(data_tps[["Original Prices","Discounts","Sale Prices"]])

#Games into csv file
game_tps = data_tps[["Title","Image","URL","Original Prices","Discounts","Sale Prices"]]
print(game_tps)
game_tps.to_csv("clean_games.csv",index=False)

#Reviews into csv file
review_tps = data_tps[["Review URL","User Score","User Reviews"]]
print(review_tps)
review_tps.to_csv("clean_reviews.csv",index=False)