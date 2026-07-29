import streamlit as st
import matplotlib.pyplot as plt
from utils import run_query

def show_visualization():
    st.subheader("Analytics & Visualization")
    
    col1, col2 = st.columns(2)
    
    # Map: Interactive map of current property listings by city
    
    with col1:
        st.text("Property Locations")
    
        map_df = run_query("SELECT Latitude, Longitude, City FROM listings")
    
        fig, ax = plt.subplots(figsize=(8, 5))
    
        for city in map_df["City"].unique():
            city_data = map_df[map_df["City"] == city]
    
        ax.scatter(
            city_data["Longitude"],
            city_data["Latitude"],
            label=city,
            alpha=0.7
        )
    
        ax.set_title("Property Listings by City")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend(title="City", bbox_to_anchor=(1.05, 1), loc="upper left")
    
        st.pyplot(fig)
    
    # Bar Chart: Number of listings or average prices by city
    with col2:
        st.text("Number of Listings by City")
    
        bar_df = run_query("SELECT City, COUNT(*) AS TotalListings FROM listings GROUP BY City ORDER BY TotalListings")
    
        fig, ax = plt.subplots(figsize=(8, 5))
    
        ax.bar(
            bar_df["City"],
            bar_df["TotalListings"]
        )
    
        ax.set_title("Number of Listings by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Total Listings")
    
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    # Pie Chart: Distribution of property types
    with col3:
        st.text("Distribution of Property Type")
    
        piechart_df = run_query("SELECT Property_Type, COUNT(*) AS TotalProperties FROM listings GROUP BY Property_Type ORDER BY TotalProperties")
    
        fig, ax = plt.subplots(figsize=(5,3))
    
        ax.pie(
            piechart_df["TotalProperties"],
            labels=piechart_df["Property_Type"],
            autopct="%1.1f%%",
            startangle=90
        )
    
        # ax.set_title("Distribution of Property Types")
        st.pyplot(fig)
    
        # Line Chart: Monthly sales and listings trend
    with col4:
        st.text("Monthly and listing trend")

        linechart_df = run_query("SELECT strftime('%Y-%m', Date_Listed) AS Month, COUNT(*) AS TotalListings FROM listings GROUP BY Month ORDER BY Month")
    
        fig, ax = plt.subplots(figsize=(8, 5))
    
        ax.plot(
            linechart_df["Month"],
            linechart_df["TotalListings"],
            marker='o'
        )
    
        # ax.set_title("Monthly Listings Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Listings")
    
        plt.xticks(rotation=45)
    
        st.pyplot(fig)
    
    # Table View: SQL query results with pagination and sorting
    col5, col6, col7 = st.columns(3)
    
    with col5:
        selected_table = st.selectbox(
            "Select a Table",
            ["Listings", "Sales", "Agents", "Buyers", "Property Attributes"]
        )
    
        if selected_table == "Listings":
            df = run_query("SELECT * FROM listings")

        elif selected_table == "Sales":
            df = run_query("SELECT * FROM sales")
        
        elif selected_table == "Agents":
            df = run_query("SELECT * FROM agents")
        
        elif selected_table == "Buyers":
            df = run_query("SELECT * FROM buyers")
        
        else:
            df = run_query("SELECT * FROM property_attributes")
    
    
    with col6:
        page_size = st.selectbox(
            "Rows per page",
            [10, 25, 50, 75, 100],
            index=0
        )
    
        total_rows = len(df)
    
        total_pages = (total_rows - 1) // page_size + 1
    
    with col7:
        page = st.number_input(
            "Page",
            min_value = 1,
            max_value = total_pages,
            value = 1
        )
    
    start = (page-1) * page_size
    
    end = start + page_size
    
    page_df = df.iloc[start:end]
    
    st.dataframe(
        page_df,
        use_container_width=True
    )