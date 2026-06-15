#Pandas clean info
import pandas as pd

data_tps = pd.read_csv("steam_deck.csv")
print(f"Original data:\n {data_tps}") #Vanilla data

#Rename some columns
data_tps = data_tps.rename(columns={"Url":"URL","ReviewUrl":"Review_URL", "Count":"User_Reviews", "Score":"User_Score","Prices":"Original_Prices"})
print(f"Changed column names:\n {data_tps}")

# Convert user reviews from strings to integers
data_tps["User_Reviews"] = (
    data_tps["User_Reviews"]
    .astype(str)
    .str.replace("User Reviews", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

data_tps["User_Reviews"] = pd.to_numeric(
    data_tps["User_Reviews"],
    downcast="integer",
    errors="coerce"
)

print(f"Integer for reviews:\n {data_tps}")

#Split "Original Prices" into a Series of lists
split_prices = data_tps['Original_Prices'].str.replace('\n', ' | ')
split_prices = split_prices.str.split(' | ',regex=False)
print(f"Split Original Prices:\n {split_prices}")

#Parse out discounts and sales prices
data_tps["Original_Prices"] = split_prices.apply(lambda x: x[1] if len(x) == 3 else ("0" if "Free" in x else x[0]))
print(f"Original Prices:\n {data_tps['Original_Prices']}")

#Create "Discounts" column
data_tps["Discounts"] = split_prices.apply(lambda x: x[0] if len(x) == 3 else "0%")
print(f"Discounts:\n {data_tps['Discounts']}")

#Sale Prices
data_tps["Sale_Prices"] = split_prices.apply(lambda x: x[2] if len(x) == 3 else ("0" if "Free" in x else x[0]))
print(f"Sale Prices:\n {data_tps['Sale_Prices']}")

print(data_tps[["Original_Prices","Discounts","Sale_Prices"]])

#Create app id to link games and reviews tables
data_tps["AppID"] = (
    data_tps["URL"]
    .str.split("/app/")
    .str[1]
    .str.split("/")
    .str[0]
)
print(data_tps[["AppID", "Title"]])

#Games into csv file
game_tps = data_tps[["AppID","Title","Image","URL","Original_Prices","Discounts","Sale_Prices"]]
# print(game_tps)
game_tps.to_csv("clean_games.csv",index=False)

#Reviews into csv file
review_tps = data_tps[["AppID","Review_URL","User_Score","User_Reviews"]]
# print(review_tps)
review_tps.to_csv("clean_reviews.csv",index=False)