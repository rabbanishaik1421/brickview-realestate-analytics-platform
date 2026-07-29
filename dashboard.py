from utils import run_query
import streamlit as st

def show_dashboard():
    # Listings
    listings = run_query("SELECT * FROM listings")

    # Listing Count
    totalListings = run_query("SELECT COUNT(*) AS TotalListings FROM listings").iloc[0]["TotalListings"]
    # print(totalListings)
    # Sales
    totalSales = run_query("SELECT COUNT(*) AS TotalSales FROM sales").iloc[0]["TotalSales"]

    # Agents
    totalAgents = run_query("SELECT COUNT(*) AS TotalAgents FROM agents").iloc[0]["TotalAgents"]

    # Buyers
    totalBuyers = run_query("SELECT COUNT(*) AS TotalBuyers FROM buyers").iloc[0]["TotalBuyers"]

    # Total Revenue
    totalRevenue = run_query("SELECT CAST(SUM(Sale_Price) AS INTEGER) AS TotalRevenue FROM sales").iloc[0]["TotalRevenue"]

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🏠 Total Listings", totalListings)
    
    with col2:
        st.metric("💰 Total Sales", totalSales)
    
    with col3:
        st.metric("🧑‍💼 Total Agents", totalAgents)
    
    with col4:
        st.metric("👥 Total Buyers", totalBuyers)
    
    with col5:
        st.metric("💵 Total Revenue", totalRevenue)
    
    # st.subheader("Introduction")
    st.subheader("Listings")
    st.dataframe(listings)