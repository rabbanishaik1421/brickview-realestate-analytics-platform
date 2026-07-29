<h2>Project Title	BrickView: Real Estate Analytics Platform</h2>
<h4>Skills take away From This Project	Python, SQL, Streamlit, Data Analysis
Domain	Real Estate, Property Analytics, Urban Development, Location Intelligence</h4>

<h4>Problem Statement</h4> 
The real estate market is vast and dynamic, with properties being listed, sold, and evaluated every day. Buyers, sellers, and agents often lack accessible tools to monitor trends, pricing, and sales performance. This project aims to build a Real Estate Listings Dashboard that uses SQL and Streamlit to:
<ul>
<li>Analyze property listings, agent performance, and sales patterns</li>
<li>Provide insights into pricing, time on market, and property types</li>
<li>Enable filtering by location, property type, price, and sales agent</li>
<li>Display interactive visuals like maps and bar charts for better understanding.</li> 
</ul>

<h4>Business Use Cases</h4>
<ul>
<li>Assist buyers and investors in making data-informed decisions</li>
<li>Help agents track sales performance and property types in demand</li>
<li>Understand pricing trends across regions and neighborhoods</li>
<li>Monitor time-on-market trends to improve sales strategies</li>
</ul>

Approach
1. Data Preparation
Use the provided datasets:
<ul>
<li>Read raw JSON files using Python</li>
<li>Flatten nested JSON structures (if any)</li>
<li>Standardize date, numeric, and boolean fields</li>
<li>Ensure date formats and price/area values are consistent</li>
</ul>

3. Database Creation
<ul>
<li>Store data in SQL using normalized relationships</li>
<li>Create views and indexes for performance</li>
</ul>

4. Data Analysis with SQL Queries
<ul>
<li> Use SQL to generate insights (detailed questions below)</li>
</ul>
5. Application Development with Streamlit
<ul>
<li>Create a user-friendly dashboard that allows:</li>
<li>Filtering based on city, property type, agent, and price range</li>
<li>Viewing maps of listings and bar/pie charts</li>
<li>Displaying SQL query outputs as tables and visuals</li>
</ul>

6. Deployment
<ul>
<li>Deploy on a local or cloud server to allow real-time access by stakeholders</li>
</ul>
Data Flow and Architecture
Data Storage:
<ul>
<li>SQL database with listings, agents, and sales etc. tables</li>
</ul>
Processing Pipeline:
<ul>
<li>Use SQL for aggregation, joins, and trend analysis</li>
</ul>
Deployment:
<ul>
<li>Streamlit UI for real-time insights and visualizations</li>
</ul>
Dataset:
<ol>
<li>Listings - listings_final_expanded.json</li>
<li>Property_attributes- property_attributes_final_expanded.json</li>
<li>Agents - agents_cleaned.json</li>
<li>Sales - sales_cleaned.csv</li>
<li>buyers  - buyers_cleaned.json </li>
</ol>

Dataset Explanation:
1️⃣ listings – Property Listing
<ul>
<li>Core property-level information</li>
<li>Column	Description</li>
<li>Listing_ID	Unique ID for the property listing</li>
<li>City	City where the property is located</li>
<li>Property_Type	Apartment, Villa, Condo, etc.</li>
<li>Price	Listed price of the property</li>
<li>Area_sqft	Property size in square feet</li>
<li>Agent_ID	Foreign key to agents</li>
<li>Listed_Date	Date property was listed</li>
<li>Latitude	</li>
<li>Longitude	</li>
</ul>

2️⃣ property_attributes – Property Attributes
<ul>
<li>One-to-one with listings</li>
<li>Column	Description</li>
<li>Attribute_ID	Unique attribute record</li>
<li>Listing_ID	FK → listings</li>
<li>Bedrooms	Number of bedrooms</li>
<li>Bathrooms	Number of bathrooms</li>
<li>Floor_Number	Floor of the property</li>
<li>Total_Floors	Total floors in building</li>
<li>Year_Built	Year of construction</li>
<li>Is_Rented	Rented or not</li>
<li>Tenant_Count	Number of tenants</li>
<li>Furnishing_Status	Furnished / Semi / Unfurnished</li>
<li>Metro_Distance_Km	Distance to metro</li>
<li>Parking_Available	Parking availability</li>
<li>Power_Backup	Power backup availability</li>
</ul>

3️⃣ agents – Real Estate Agents
<ul>
<li>Column	Description</li>
<li>Agent_ID	Unique agent identifier</li>
<li>Name	Agent name</li>
<li>City	Operating city</li>
<li>Contact	Phone/email</li>
<li>Commission_Rate	Commission %</li>
<li>Deals_Closed	Total deals</li>
<li>Rating	Client rating</li>
<li>Experience_Years	Years of experience</li>
<li>Avg_Closing_Days	Avg deal closing time</li>
</ul>

5️⃣ sales – Property Sales
<ul>
<li>Column	Description</li>
<li>Sale_ID	Unique sale ID</li>
<li>Listing_ID	FK → listings</li>
<li>Sale_Date	Sale date</li>
<li>Sale_Price	Final sale price</li>
<li>Days_On_Market	Time to sell</li>
</ul>

6️⃣ buyers – Buyer Information
<ul>
<li>Column	Description</li>
<li>Buyer_ID	Buyer identifier</li>
<li>Sale_ID	FK → sales</li>
<li>Buyer_Type	Investor / End User</li>
<li>Payment_Mode	Cash / UPI / Bank / Cheque</li>
<li>Loan_Taken	Loan taken or not</li>
<li>Loan_Provider	Bank name</li>
<li>Loan_Amount	Loan amount</li>
</ul>
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
18. Which properties are currently unsold?
🧑‍💼 Agent Performance
29.	Which agents have closed the most sales?
20.	Who are the top agents by total sales revenue?
21.	Which agents close deals fastest?
22.	Does experience correlate with deals closed?
23.	Do agents with higher ratings close deals faster?
24.	What is the average commission earned by each agent?
25.	Which agents currently have the most active listings?
🧍 Buyer & Financing Behavior
26. What percentage of buyers are investors vs end users?
27. Which cities have the highest loan uptake rate?
28. What is the average loan amount by buyer type?
29. Which payment mode is most commonly used?
30. Do loan-backed purchases take longer to close?

🧮 Streamlit App Features
🎛️ Filters Page
<ul>
<li>City – Multi-select (e.g., filter listings in New York, San Francisco, etc.)</li>
<li>Property Type – Dropdown (Apartment, Villa, Condo, etc.)</li>
<li>Price Range – Slider for min and max price</li>
<li>Agent – Searchable dropdown to filter by agent</li>
<li>Date Range – Date picker for Listed Date or Sale Date</li>
</ul>

📈 Visualizations Page
<ul>
<li>Map: Interactive map of current property listings by city</li>
<li>Bar Chart: Number of listings or average prices by city</li>
<li>Pie Chart: Distribution of property types</li>
<li>Line Chart: Monthly sales and listings trend</li>
<li>Table View: SQL query results with pagination and sorting</li>
</ul>

3️⃣ CRUD Operations Page
<li>Implement complete CRUD (Create, Read, Update, Delete) operations.</li>
<ul>
<li>Apply CRUD functionality to all database tables.</li>
<li>Each table must support:</li>
<li>View records</li>
<li>Add new records</li>
<li>Update existing records</li>
<li>Delete records</li>
</ul>

4️⃣ SQL Queries Display Page
<ul>
<li>Show all SQL queries in drop-down format.</li>
<li>Each drop-down must include:</li>
<li>o	The SQL query</li>
<li>o	The output displayed as a table.</li>
</ul>
Results 
<ul>
<li>✔️ A full-featured Streamlit app to explore real estate data</li>
<li>✔️ 15+ SQL queries providing insights into price, agent performance, and property types</li>
<li>✔️ Visualizations and filters for interactive data exploration</li>
<li>✔️ Clean database schema optimized for real-time querying</li>
</ul>

Project Evaluation Metrics:
<ul>
<li>Proper SQL schema and normalized tables</li>
<li>Accuracy of SQL queries and aggregations</li>
<li>Quality and completeness of Streamlit visualizations</li>
<li>Functional filters and interactivity</li>
<li>User-friendly interface and navigation</li>
</ul>

    


