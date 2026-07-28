import pandas as pd

# Listings
listings = pd.read_json("../raw/listings_final_expanded.json")
listings["Date_Listed"] = pd.to_datetime(listings["Date_Listed"])
listings["Price"] = listings["Price"].fillna(0).astype(int)
print(listings)
# print(listings.info())

# Property Attributes
property_attributes = pd.read_json("../raw/property_attributes_final_expanded.json")

# Agents
agents = pd.read_json("../raw/agents_cleaned.json")

# Sales
sales = pd.read_csv("../raw/sales_cleaned.csv")
sales["Date_Sold"] = pd.to_datetime(sales["Date_Sold"])

# Buyers
buyers = pd.read_json("../raw/buyers_cleaned.json")