import streamlit as st
from utils import run_query

def showfilter():
    st.subheader("Filters & Explorer")

    property_type_df = run_query("SELECT DISTINCT Property_Type FROM listings")
    property_types = property_type_df["Property_Type"].tolist()

    # Filters
    city_df = run_query("SELECT DISTINCT City FROM listings")
    cities = city_df["City"].tolist()

    price_df = run_query("SELECT MIN(Price) AS MinPrice, MAX(Price) AS MaxPrice FROM listings")
    MinPrice = price_df.iloc[0]['MinPrice']
    MaxPrice = price_df.iloc[0]['MaxPrice']
    
    date_df = run_query("SELECT MIN(Date_Listed) AS MinDate, MAX(Date_Listed) AS MaxDate FROM listings")
    MinDate = date_df.iloc[0]["MinDate"]
    MaxDate = date_df.iloc[0]["MaxDate"]

    agent_df = run_query("""
    SELECT
        Agent_ID,
        Name
    FROM agents
    ORDER BY Name
    """)
    agent_df["Display"] = (
        agent_df["Agent_ID"] + " - " + agent_df["Name"]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        selected_cities = st.multiselect(
            "📍 Select City",
            cities
        )

    with col2:
        selected_property_type = st.selectbox(
            "🏠 Select Property Type",
            property_types,
            index=None,
            placeholder="Select Property Type"
        )

    with col3:
        selected_price = st.slider(
            "💰 Select Price Range",
            min_value=MinPrice,
            max_value=MaxPrice,
            value=(MinPrice, MaxPrice),
            step=10000
        )

    with col4:
        selected_agent = st.selectbox(
            "👨‍💼 Select Agent",
            ["All"] + agent_df["Display"].tolist()
        )

    with col5:
        selected_date = st.date_input(
            "📅 Listed Date Range",
            min_value=MinDate,
            max_value=MaxDate,
            value=(MinDate, MaxDate)
        )

    query = "SELECT * FROM listings WHERE 1=1"
    params = []

    # City Filter
    if selected_cities:
        placeholders = ",".join(["?"]*len(selected_cities))

        query += f" AND City in ({placeholders})"

        params.extend(selected_cities)

    # Property Type Filter
    if selected_property_type:
        query += " AND Property_Type = ?"
        params.append(selected_property_type)

    # Price Filter
    if selected_price:
        query += " AND Price BETWEEN ? AND ?"
        params.extend(selected_price)

    # Agents Filter
    if selected_agent != "All":
        agent_id = selected_agent.split(" - ")[0]

        query += " AND Agent_ID = ?"
        params.append(agent_id)

    # Date Filter
    if len(selected_date) == 2:
        query += " AND Date_Listed BETWEEN ? AND ?"
        params.append(selected_date[0].strftime("%Y-%m-%d"))
        params.append(selected_date[1].strftime("%Y-%m-%d"))

    listings = run_query(query, params)        
        
    st.subheader("Listings")
    st.dataframe(listings)    