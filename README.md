<h2>Project Title	BrickView: Real Estate Analytics Platform</h2>
<h4>Skills take away From This Project	Python, SQL, Streamlit, Data Analysis
Domain	Real Estate, Property Analytics, Urban Development, Location Intelligence</h4>

Problem Statement 
The real estate market is vast and dynamic, with properties being listed, sold, and evaluated every day. Buyers, sellers, and agents often lack accessible tools to monitor trends, pricing, and sales performance. This project aims to build a Real Estate Listings Dashboard that uses SQL and Streamlit to:
•	Analyze property listings, agent performance, and sales patterns
•	Provide insights into pricing, time on market, and property types
•	Enable filtering by location, property type, price, and sales agent
•	Display interactive visuals like maps and bar charts for better understanding. 

Business Use Cases
•	Assist buyers and investors in making data-informed decisions
•	Help agents track sales performance and property types in demand
•	Understand pricing trends across regions and neighborhoods
•	Monitor time-on-market trends to improve sales strategies

Approach
1. Data Preparation
Use the provided datasets:
•	Read raw JSON files using Python
•	Flatten nested JSON structures (if any)
•	Standardize date, numeric, and boolean fields
•	Ensure date formats and price/area values are consistent

2. Database Creation
•	Store data in SQL using normalized relationships
•	Create views and indexes for performance

3. Data Analysis with SQL Queries
Use SQL to generate insights (detailed questions below)

4. Application Development with Streamlit
Create a user-friendly dashboard that allows:
•	Filtering based on city, property type, agent, and price range
•	Viewing maps of listings and bar/pie charts
•	Displaying SQL query outputs as tables and visuals

5. Deployment
Deploy on a local or cloud server to allow real-time access by stakeholders

Data Flow and Architecture
Data Storage:
•	SQL database with listings, agents, and sales etc. tables

Processing Pipeline:
•	Use SQL for aggregation, joins, and trend analysis

Deployment:
•	Streamlit UI for real-time insights and visualizations

Dataset:
1.	Listings - listings_final_expanded.json
2.	Property_attributes- property_attributes_final_expanded.json
3.	Agents - agents_cleaned.json
4.	Sales - sales_cleaned.csv
5.	buyers  - buyers_cleaned.json 

Dataset Explanation:
1️⃣ listings – Property Listings
Core property-level information
Column	Description
Listing_ID	Unique ID for the property listing
City	City where the property is located
Property_Type	Apartment, Villa, Condo, etc.
Price	Listed price of the property
Area_sqft	Property size in square feet
Agent_ID	Foreign key to agents
Listed_Date	Date property was listed

Latitude	
Longitude	

2️⃣ property_attributes – Property Attributes
One-to-one with listings
Column	Description
Attribute_ID	Unique attribute record
Listing_ID	FK → listings
Bedrooms	Number of bedrooms
Bathrooms	Number of bathrooms
Floor_Number	Floor of the property
Total_Floors	Total floors in building
Year_Built	Year of construction
Is_Rented	Rented or not
Tenant_Count	Number of tenants
Furnishing_Status	Furnished / Semi / Unfurnished
Metro_Distance_Km	Distance to metro
Parking_Available	Parking availability
Power_Backup	Power backup availability

3️⃣ agents – Real Estate Agents
Column	Description
Agent_ID	Unique agent identifier
Name	Agent name
City	Operating city
Contact	Phone/email
Commission_Rate	Commission %
Deals_Closed	Total deals
Rating	Client rating
Experience_Years	Years of experience
Avg_Closing_Days	Avg deal closing time

5️⃣ sales – Property Sales
Column	Description
Sale_ID	Unique sale ID
Listing_ID	FK → listings
Sale_Date	Sale date
Sale_Price	Final sale price
Days_On_Market	Time to sell

6️⃣ buyers – Buyer Information
Column	Description
Buyer_ID	Buyer identifier
Sale_ID	FK → sales
Buyer_Type	Investor / End User
Payment_Mode	Cash / UPI / Bank / Cheque
Loan_Taken	Loan taken or not
Loan_Provider	Bank name
Loan_Amount	Loan amount

📊 Key SQL Questions & Queries
📊 Property & Pricing Analysis
1.	What is the average listing price by city?
2.	What is the average price per square foot by property type?
3.	How does furnishing status impact property prices?
4.	Do properties closer to metro stations command higher prices?
5.	Are rented properties priced differently from non-rented ones?
6.	How do bedrooms and bathrooms affect pricing?
7.	Do properties with parking and power backup sell at higher prices?
8.	How does year built influence listing price?
9.	Which cities have the highest average property prices?
10.	How are properties distributed across price buckets?

⏱️ Sales & Market Performance
11.	What is the average days on market by city?
12.	Which property types sell the fastest?
13.	What percentage of properties are sold above listing price?
14.	What is the sale-to-list price ratio by city?
15.	Which listings took more than 90 days to sell?
16.	How does metro distance affect time on market?
17.	What is the monthly sales trend?
18.	Which properties are currently unsold?

🧑‍💼 Agent Performance
19.	Which agents have closed the most sales?
20.	Who are the top agents by total sales revenue?
21.	Which agents close deals fastest?
22.	Does experience correlate with deals closed?
23.	Do agents with higher ratings close deals faster?
24.	What is the average commission earned by each agent?
25.	Which agents currently have the most active listings?

🧍 Buyer & Financing Behavior
26.	What percentage of buyers are investors vs end users?
27.	Which cities have the highest loan uptake rate?
28.	What is the average loan amount by buyer type?
29.	Which payment mode is most commonly used?
30.	Do loan-backed purchases take longer to close?

🧮 Streamlit App Features
🎛️ Filters Page
•	City – Multi-select (e.g., filter listings in New York, San Francisco, etc.)
•	Property Type – Dropdown (Apartment, Villa, Condo, etc.)
•	Price Range – Slider for min and max price
•	Agent – Searchable dropdown to filter by agent
•	Date Range – Date picker for Listed Date or Sale Date
etc.

📈 Visualizations Page
•	Map: Interactive map of current property listings by city
•	Bar Chart: Number of listings or average prices by city
•	Pie Chart: Distribution of property types
•	Line Chart: Monthly sales and listings trend
•	Table View: SQL query results with pagination and sorting
etc.

3️⃣ CRUD Operations Page
•	Implement complete CRUD (Create, Read, Update, Delete) operations.

•	Apply CRUD functionality to all database tables.
•	Each table must support:
o	View records
o	Add new records
o	Update existing records
o	Delete records

4️⃣ SQL Queries Display Page
•	Show all SQL queries in drop-down format.
•	Each drop-down must include:
o	The SQL query
o	The output displayed as a table.

Results 
•	✔️ A full-featured Streamlit app to explore real estate data
•	✔️ 15+ SQL queries providing insights into price, agent performance, and property types
•	✔️ Visualizations and filters for interactive data exploration
•	✔️ Clean database schema optimized for real-time querying
 
Project Evaluation Metrics:
•	Proper SQL schema and normalized tables
•	Accuracy of SQL queries and aggregations
•	Quality and completeness of Streamlit visualizations
•	Functional filters and interactivity
•	User-friendly interface and navigation


    


