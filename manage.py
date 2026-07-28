import pandas as pd

"""##################"""
"""Step 1: Fetch Data"""
"""##################"""

# Listings
listings = pd.read_json("data/raw/listings_final_expanded.json")

# Property Attributes
property_attributes = pd.read_json("data/raw/property_attributes_final_expanded.json")

# Agents
agents = pd.read_json("data/raw/agents_cleaned.json")

# Sales
sales = pd.read_csv("data/raw/sales_cleaned.csv")

# Buyers
buyers = pd.read_json("data/raw/buyers_cleaned.json")

"""##################"""
"""Step 2: Data Clean"""
"""##################"""
# Listings
listings["Date_Listed"] = pd.to_datetime(listings["Date_Listed"])
listings["Price"]   = listings["Price"].fillna(0).astype(int)
listings["Sqft"]    = listings["Sqft"].fillna(0).astype(int)

# Sales
sales["Date_Sold"]      = pd.to_datetime(sales["Date_Sold"])
sales['Sale_ID']        = ["S{:05d}".format(i) for i in range(1, len(sales)+1)]
sales["Days_on_Market"] = sales["Days_on_Market"].fillna(0).astype(int)
sales["Sale_Price"]     = sales["Sale_Price"].fillna(0).astype(int)

"""##########################################"""
"""Step 3: Store Cleaned Data to the Database"""
"""##########################################"""
# Import sqlite database library
import sqlite3

# Create Database
conn = sqlite3.connect("brickviewdb")
if not conn:
    print("Database not connected")

cursor = conn.cursor()

# Agents Table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS agents(
        Agent_ID TEXT PRIMARY KEY,
        Name TEXT,
        Phone TEXT,
        Email TEXT,
        commission_rate REAL,
        deals_closed INTEGER,
        rating REAL,
        experience_years INTEGER,
        avg_closing_days INTEGER
    )
"""
)

# Insert Agent Records to the Agents tabel from the agents dataset
for _, row in agents.iterrows():
    cursor.execute(
        """
        INSERT INTO agents(Agent_ID, Name, Phone, Email, commission_rate, deals_closed, rating, experience_years, avg_closing_days) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row["Agent_ID"], row["Name"], row["Phone"], row["Email"], row["commission_rate"], row["deals_closed"], row["rating"], row["experience_years"], row["avg_closing_days"])
    )

agents_df = pd.read_sql("SELECT * FROM agents", conn)
# print(agents_df)

# Listings Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings(
        Listing_ID TEXT PRIMARY KEY,
        City TEXT,
        Property_Type TEXT,
        Price INTEGER,
        Sqft INTEGER,
        Date_Listed DATE,
        Latitude REAL,
        Longitude REAL,
        Agent_ID TEXT,
        FOREIGN KEY (Agent_ID) REFERENCES agents(Agent_ID)
    )
""")

# Insert Listings Records
for _,row in listings.iterrows():
    cursor.execute("""
        INSERT INTO listings(Listing_ID, City, Property_Type, Price, Sqft, Date_Listed, Latitude, Longitude, Agent_ID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
        (row["Listing_ID"], row["City"], row["Property_Type"], row["Price"], row["Sqft"], row["Date_Listed"].strftime("%Y-%m-%d"), row["Latitude"], row["Longitude"], row["Agent_ID"])
    )

listings_df = pd.read_sql("SELECT * FROM listings", conn)
print(listings_df)

# Create Property Attributes Table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS property_attributes(
        attribute_id INTEGER, 
        listing_id TEXT NOT NULL, 
        bedrooms INTEGER, 
        bathrooms INTEGER, 
        floor_number INTEGER,        
        total_floors INTEGER,
        year_built INTEGER,
        is_rented BOOLEAN,
        tenant_count INTEGER,
        furnishing_status TEXT NOT NULL, 
        metro_distance_km REAL, 
        parking_available BOOLEAN, 
        power_backup BOOLEAN,
        FOREIGN KEY(listing_id) REFERENCES listings(Listing_ID)
    )
    """
)

for _,row in property_attributes.iterrows():
    cursor.execute(
        """INSERT INTO property_attributes(attribute_id, listing_id, bedrooms, bathrooms, floor_number, total_floors, year_built, is_rented, tenant_count, furnishing_status, metro_distance_km, parking_available, power_backup) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (row["attribute_id"], row["listing_id"], row["bedrooms"], row["bathrooms"], row["floor_number"], row["total_floors"], row["year_built"], row["is_rented"], row["tenant_count"], row["furnishing_status"], row["metro_distance_km"], row["parking_available"], row["power_backup"])
    )

property_df = pd.read_sql("SELECT is_rented,* FROM property_attributes", conn)
# print(property_df)

# Create Sales Table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sales(
        Sale_ID TEXT PRIMARY KEY,
        Listing_ID TEXT NOT NULL,
        Sale_Price INTEGER,
        Date_Sold DATE,
        Days_on_Market INTEGER
    )
    """
)

for _,row in sales.iterrows():
    cursor.execute("""INSERT INTO sales(Sale_ID, Listing_ID, Sale_Price, Date_Sold, Days_on_Market) VALUES(?, ?, ?, ?, ?)
    """, 
    (row["Sale_ID"], row["Listing_ID"], row["Sale_Price"], row["Date_Sold"].strftime("%Y-%m-%d"), row["Days_on_Market"]))

sales_df = pd.read_sql("SELECT * FROM sales", conn)
# print(sales_df)

# Create Buyers table and Insert Buyers data
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS buyers(
        buyer_id INTEGER PRIMARY KEY,
        sale_id TEXT NOT NULL,
        buyer_type TEXT NOT NULL,
        payment_mode TEXT NOT NULL,
        loan_taken BOOLEAN,
        loan_provider TEXT,
        loan_amount INTEGER,
        FOREIGN KEY(sale_id) REFERENCES sales(Sale_ID)        
    )
    """
)

for _,row in buyers.iterrows():
    cursor.execute(
        """INSERT INTO buyers(buyer_id, sale_id, buyer_type, payment_mode, loan_taken, loan_provider, loan_amount) VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (row["buyer_id"], row["sale_id"], row["buyer_type"], row["payment_mode"], row["loan_taken"], row["loan_provider"], row["loan_amount"])
    )

buyers_df = pd.read_sql("SELECT * FROM property_attributes", conn)
# print(buyers_df)
conn.commit()

# import sqlite3
# conn = sqlite3.connect("brickviewdb")
# if not conn:
#     print("Database not connected")

# cursor = conn.cursor()

# cursor.execute("DROP TABLE buyers")
# cursor.execute("DROP TABLE sales")
# cursor.execute("DROP TABLE property_attributes")
# cursor.execute("DROP TABLE listings")
# cursor.execute("DROP TABLE agents")
# conn.commit()

