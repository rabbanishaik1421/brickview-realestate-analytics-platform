import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="BrickView Real Estate",
    page_icon="🏠",
    layout="wide"
)

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# Database Connection
conn = sqlite3.connect("brickviewdb")
cursor = conn.cursor()

# Pandas custom helper functions
def run_query(query):
    return pd.read_sql(query, conn)

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

# Filters
city_df = run_query("SELECT DISTINCT City FROM listings")
cities = city_df["City"].tolist()

property_type_df = run_query("SELECT DISTINCT Property_Type FROM listings")
property_types = property_type_df["Property_Type"].tolist()

price_df = run_query("SELECT MIN(Price) AS MinPrice, MAX(Price) AS MaxPrice FROM listings")
MinPrice = price_df.iloc[0]['MinPrice']
MaxPrice = price_df.iloc[0]['MaxPrice']

date_df = run_query("SELECT MIN(Date_Listed) AS MinDate, MAX(Date_Listed) AS MaxDate FROM listings")
MinDate = date_df.iloc[0]["MinDate"]
MaxDate = date_df.iloc[0]["MaxDate"]

# Visualization Queries
map_df = run_query("""
    SELECT
        Latitude AS lat,
        Longitude AS lon,
        City,
        Price,
        Property_Type
    FROM listings
    """)

# bar chart query
numlistings = run_query("SELECT City, COUNT(*) AS TotalListings FROM listings")

# st.subheader("Location Data")
# st.dataframe(map_df)

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

# sidebar
st.sidebar.title("BrickView")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Introduction",
        "Filters & Explorer",
        "Visualization",
        "Crud Operations",
        "SQL Queries"
    ]
)

########################
##### INTRODUCTION #####
########################
if menu == "Introduction":        
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView Analytics Dashboard"

    st.markdown(
        """
        <style>
        .re-title{
            text-align:center;
            margin-bottom:15px;
        }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
    """, unsafe_allow_html=True
    )

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

##############################
##### Filters & Explorer #####
##############################

elif menu == "Filters & Explorer":
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView Analytics Dashboard"
    
    st.markdown(
            """
        <style>
        .re-title{
            text-align:center;
            margin-bottom:15px;
        }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.subheader("Filters & Explorer")

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

    listings = pd.read_sql(query, conn, params=params)        
    
    st.subheader("Listings")
    st.dataframe(listings)    

#########################
##### VISUALIZATION #####
#########################

elif menu == "Visualization":
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView Analytics Dashboard"
        
    st.markdown(
        """
        <style>
            .re-title{
                text-align:center;
                margin-bottom:15px;
            }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
        """, unsafe_allow_html=True
    )

    st.subheader("Analytics & Visualization")

    col1, col2 = st.columns(2)

    # Map: Interactive map of current property listings by city

    with col1:
        st.subheader("Property Locations")

        map_df = run_query("""
            SELECT
                Latitude,
                Longitude,
                City
            FROM listings
        """)

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
        st.subheader("Number of Listings by City")

        bar_df = run_query(
            """
            SELECT 
                City, 
                COUNT(*) AS TotalListings 
            FROM listings 
            GROUP BY City
            ORDER BY TotalListings
        """
        )

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
        st.subheader("Distribution of Property Type")

        piechart_df = run_query(
            """
            SELECT 
                Property_Type,
                COUNT(*) AS TotalProperties
            FROM 
                listings
            GROUP BY Property_Type
            ORDER BY TotalProperties
        """
        )

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
        st.subheader("Monthly and listing trend")

        linechart_df = run_query(
            """
            SELECT 
                strftime('%Y-%m', Date_Listed) AS Month,
                COUNT(*) AS TotalListings
            FROM 
                listings
            GROUP BY Month
            ORDER BY Month
        """
        )

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


###########################
##### Crud Operations #####
###########################

elif menu == "Crud Operations":
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView CRUD Operations"
    
    st.markdown(
        """
        <style>
            .re-title{
                text-align:center;
                margin-bottom:15px;
            }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
        """, unsafe_allow_html=True
    )
        
    st.subheader("Crud Operations")

    col8, col9, col10 = st.columns(3)

    with col8:
        selected_table = st.selectbox(
            "Select a Table",
            ["Listings", "Sales", "Agents", "Buyers", "Property Attributes"]
        )

    with col9:
        operation = st.radio(
            "Choose operation",
            ["View", "Add", "Update", "Delete"],
            horizontal=True
        )

    ####################################### 
    # LISTINGS CRUD OPREATIONS #    
    #######################################
    if selected_table == "Listings" and operation == "View":
        st.text("View Listings")
        crud_list = run_query("SELECT * FROM listings")
        st.dataframe(crud_list)

    # ADD LISTING
    if selected_table == "Listings" and operation == "Add":
        st.text("Add Listing:")   

        with st.form("add_listing_form"):
            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)

            with col1:
                listing_id = st.text_input("Listing ID")     
                city = st.text_input("City")
                property_type = st.selectbox(
                    "Property Type",
                    ["Apartment", "Villa", "House", "Condo", "Townhouse"]
                )

            with col2:            
                price       = st.text_input("Price")
                sqft        = st.text_input("Sqft")
                date_listed = st.date_input("Date Listed")

            with col3:
                latitude    = st.text_input("Latitude")            
                longitude   = st.text_input("Longitude")
                agents = run_query("SELECT Agent_ID FROM agents")
                agent       = st.selectbox(
                    "Agent",
                    agents["Agent_ID"]
                )

            with col4:
                submit = st.form_submit_button("Add Listing", type="primary")

        if submit:
            if (
                listing_id.strip() == "" or city.strip() == "" or property_type.strip() == "" or price.strip() == "" or sqft.strip() == "" or date_listed == "" or agent.strip() == "" or latitude.strip() == "" or longitude.strip() == ""
            ):
                st.error("Please fill in all the required fields.")
            else:
                cursor.execute(
                    """
                    INSERT INTO listings(Listing_ID, City, Property_Type, Price, Sqft, Date_Listed, Agent_ID, Latitude, Longitude) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (listing_id, city, property_type, price, sqft, date_listed, agent, latitude, longitude)
                )

                conn.commit()

                st.success("Listing added successfully.")

    # UPDATE LISTING
    if selected_table == "Listings" and operation == "Update":
        st.text("Update Listing:")

        listing_df = run_query("""
            SELECT Listing_ID
            FROM listings
            ORDER BY Listing_ID
        """)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            selected_listing = st.selectbox(
                "Select Listing",
                listing_df["Listing_ID"]
            )

        listing = pd.read_sql(
            """
            SELECT *
            FROM listings
            WHERE Listing_ID = ?
            """,
            conn,
            params=(selected_listing,)
        )

        with st.form("update_listing_form"):
            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)
        
            with col1:
                listing_id = st.text_input("Listing ID", value=listing.iloc[0]["Listing_ID"], disabled=True)     
                city = st.text_input("City", value=listing.iloc[0]["City"])
                property_type = st.selectbox(
                    "Property Type",
                    ["Apartment", "Villa", "House", "Condo", "Townhouse"]
                )
        
                with col2:            
                    price       = st.text_input("Price", value=listing.iloc[0]["Price"])
                    sqft        = st.text_input("Sqft", value=listing.iloc[0]["Sqft"])
                    date_listed = st.date_input("Date Listed", value=listing.iloc[0]["Date_Listed"])
        
                with col3:
                    latitude    = st.text_input("Latitude", value=listing.iloc[0]["Latitude"])            
                    longitude   = st.text_input("Longitude", value=listing.iloc[0]["Longitude"])
                    agent_df = run_query("""
                        SELECT Agent_ID
                        FROM agents
                    """)

                    agent_index = agent_df[
                        agent_df["Agent_ID"] == listing.iloc[0]["Agent_ID"]
                    ].index[0]

                    agent_id = st.selectbox(
                        "Agent",
                        agent_df["Agent_ID"],
                        index=agent_index
                    )
        
                with col4:
                    update = st.form_submit_button("Update Listing")

        if update:
            if (
                listing_id.strip() == "" or city.strip() == "" or property_type.strip() == "" or price.strip() == "" or sqft.strip() == "" or date_listed == "" or agent_id.strip() == "" or latitude.strip() == "" or longitude.strip() == ""
            ):
                st.error("Please fill in all the required fields.")
            else:
                cursor.execute(
                    """
                    UPDATE listings
                    SET
                        City=?, Property_Type=?, Price=?, Sqft=?, Date_Listed=?, Latitude=?, Longitude=?, Agent_ID=?
                        WHERE Listing_ID=?
                        """,
                        (
                            city, property_type, price, sqft, date_listed.strftime("%Y-%m-%d"), latitude,
                            longitude, agent_id, selected_listing
                        )
                )

                conn.commit()
            
                st.success("Listing updated successfully.")

    # DELETE LISTING
    if selected_table == "Listings" and operation == "Delete":
        st.text("Delete Listing:")

        listings = run_query("SELECT Listing_ID FROM listings")

        selected_list = st.selectbox(
            "Select Listing ID",
            listings["Listing_ID"],
            width=200
        )

        selected_list_df = pd.read_sql(
            """
            SELECT *
            FROM listings
            WHERE Listing_ID=?
            """,
            conn,
            params=(selected_list,)
        )

        if selected_list:
            st.dataframe(
                selected_list_df,
                use_container_width=True,
                hide_index=True
            )

            confirm = st.checkbox(
                "I understand that this action cannot be undone."
            )

            if st.button(
                "Delete Listing",
                type="primary"
            ):

                if not confirm:
                    st.warning("Please confirm before deleting.")
                else:

                    cursor.execute(
                        """
                        DELETE FROM listings
                        WHERE Listing_ID=?
                        """,
                        (selected_list,)
                    )

                    conn.commit()

                    st.success("Listing deleted successfully.")

                    st.rerun()

    #########################
    # SALES CRUD OPREATIONS #    
    #########################
    if selected_table == "Sales" and operation == "View":
        st.text("View Sales:")
        crud_list = run_query("SELECT * FROM sales")
        st.dataframe(crud_list)

    if selected_table == "Sales" and operation == "Add":
        st.text("Add Sale:")
        with st.form("add_sale_form"):
            
            col1, col2, col3, col4, col5 = st.columns(5)

            sales = pd.read_sql("""SELECT COUNT(*) AS RowNo, MAX(Sale_ID) AS MaxSale FROM sales""", conn)
            rowno = sales.iloc[0]["RowNo"] + 1
            sale_id = f"S{rowno:05d}"

            listings = pd.read_sql("SELECT Listing_ID FROM listings", conn)

            with col1:
                listing_id = st.selectbox("Listing ID", listings)

            with col2:
                sale_price = st.text_input("Sale Price")

            with col3:
                date_sold = st.date_input("Date Sold")

            with col4: 
                days_on_market = st.number_input("Days on Market")

            with col5:
                sale_id = st.text_input("Sale Id", value=sale_id, disabled=True)

            submit = st.form_submit_button("Add Sale", type="primary")

        if submit:
            if(
                listing_id.strip() == "" or sale_price == "" or date_sold == "" or days_on_market == ""
            ):
                st.error("Please fill all the required fields")
            else:
                cursor.execute(
                    """
                    INSERT INTO sales(Sale_ID, Listing_ID, Sale_Price, Date_Sold, Days_On_Market) VALUES(?, ?, ?, ?, ?)
                    """, (sale_id, listing_id, sale_price, date_sold, days_on_market)
                )

                conn.commit()

                st.success("New sale record added successfully")

                st.rerun()
                
    if selected_table == "Sales" and operation == "Update":
        st.text("Update Sale:")
        sales = pd.read_sql("SELECT Sale_ID FROM sales WHERE Sale_ID IS NOT NULL", conn)
        sale_id = st.selectbox(
            "Select Sale ID",
            sales,
            index=None,
            placeholder="Choose a Sale ID",
            width=200
        )

        if sale_id:
            saleinfo = pd.read_sql("SELECT * FROM sales WHERE Sale_ID=?", conn, params=(sale_id,))

            listings = pd.read_sql("SELECT Listing_ID FROM listings", conn)

            with st.form("update_sale_form"):
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    listings = pd.read_sql(
                        "SELECT Listing_ID FROM listings ORDER BY Listing_ID",
                        conn
                    )

                    listing_list = listings["Listing_ID"].tolist()

                    current_listing = saleinfo.iloc[0]["Listing_ID"]

                    current_index = listing_list.index(current_listing)

                    listing_id = st.selectbox(
                        "Listing ID",
                        listing_list,
                        index=current_index
                    )

                with col2:
                    sale_price = st.number_input("Sale Price", value=saleinfo.iloc[0]["Sale_Price"])

                with col3:
                    date_sold = st.date_input("Date Sold", value=saleinfo.iloc[0]["Date_Sold"])

                with col4:
                    days_on_market = st.number_input("Days on Market", value=saleinfo.iloc[0]["Days_on_Market"])

                with col5:
                    sid = st.text_input("Sale Id", value=saleinfo.iloc[0]["Sale_ID"], disabled=True)

                update_sale = st.form_submit_button("Update Sale", type="primary")

                if update_sale:
                    cursor.execute(
                        """
                        UPDATE sales SET Listing_ID=?, Sale_Price=?, Date_Sold=?, Days_on_Market=? WHERE Sale_ID=?
                    """, (listing_id, sale_price, date_sold, days_on_market, sid)
                    )

                    conn.commit()

                    st.success("Sale data has been updated successfully!")

                    st.rerun()

    if selected_table == "Sales" and operation == "Delete":
        sales = pd.read_sql("SELECT * FROM sales", conn)
        st.text("Delete Sale:")

        sale_id = st.selectbox(
            "Select Sale ID", 
            sales, 
            width=200,
            index=None,
            placeholder="Select Sale"
        )

        if sale_id:
            saleinfo = pd.read_sql("SELECT * FROM sales WHERE Sale_ID=?", conn, params=(sale_id,))

            st.dataframe(saleinfo, hide_index=True)

            confirm = st.checkbox("Are you sure, you want to delete this record")

            delete_sale = st.button("Delete Sale", type="primary")

            if delete_sale:
                if not confirm:
                    st.error("Please tick on checkbox confirmation")
                else:
                    cursor.execute("""DELETE FROM sales WHERE Sale_ID=?""", (sale_id,))

                    conn.commit()
                    st.success("Selected sale record has been deleted successfully")
                    st.rerun()

    # Agents Crud Operations
    if selected_table == "Agents" and operation == "View":
        st.text("List of Agents:")
        crud_list = run_query("SELECT * FROM agents")
        st.dataframe(crud_list, hide_index=True)

    if selected_table == "Agents" and operation == "Add":
        st.text("Add Agent:")

        with st.form("add_agent_form"):
            col1, col2, col3, col4 = st.columns(4)

            agents  = pd.read_sql("""SELECT COUNT(*) AS RowNo FROM agents""", conn)
            rowno   = agents.iloc[0]["RowNo"] + 1
            agentid = f"A{rowno:05d}"

            with col1:
                name = st.text_input("Name")
                phone = st.text_input("Phone")

            with col2:
                email = st.text_input("Email")
                commission_rate = st.number_input("Commission Rate")

            with col3:
                deals_closed = st.number_input("Deals Closed")
                rating = st.number_input("Rating")

            with col4:
                exp_years = st.number_input("Experience Years")
                avg_closing_days = st.number_input("Avg closing days")

            submit = st.form_submit_button("Submit", type="primary")

            if submit:
                cursor.execute(
                    """
                    INSERT INTO agents(Agent_ID, Name, Phone, Email, commission_rate, deals_closed, rating, experience_years, avg_closing_days) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (agentid, name, phone, email, commission_rate, deals_closed, rating, exp_years, avg_closing_days)
                )

                conn.commit()
                st.success("New agent record added successfully.")
                st.rerun()

    if selected_table == "Agents" and operation == "Update":
        st.text("Update Agent:")

        agents = pd.read_sql("SELECT Agent_ID FROM agents", conn)

        agent_id = st.selectbox(
            "Select Agent",
            agents,
            width=200,
            placeholder="Select",
            index=None
        )

        if agent_id:
            with st.form("add_agent_form"):
                col1, col2, col3, col4 = st.columns(4)
            
                agentinfo = pd.read_sql("SELECT * FROM agents WHERE Agent_ID=?", conn, params=(agent_id,))
            
                with col1:
                    name = st.text_input("Name", value=agentinfo.iloc[0]["Name"])
                    phone = st.text_input("Phone", value=agentinfo.iloc[0]["Phone"])
            
                with col2:
                    email = st.text_input("Email", value=agentinfo.iloc[0]["Email"])
                    commission_rate = st.number_input("Commission Rate", value=agentinfo.iloc[0]["commission_rate"])
            
                with col3:
                    deals_closed = st.number_input("Deals Closed", value=agentinfo.iloc[0]["deals_closed"])
                    rating = st.number_input("Rating", value=agentinfo.iloc[0]["rating"])
            
                with col4:
                    exp_years = st.number_input("Experience Years", value=agentinfo.iloc[0]["experience_years"])
                    avg_closing_days = st.number_input("Avg closing days", value=agentinfo.iloc[0]["avg_closing_days"])
            
                update = st.form_submit_button("Update", type="primary")

                if update:
                    cursor.execute("""
                    UPDATE agents SET Name=?, Phone=?, Email=?, commission_rate=?, deals_closed=?, rating=?, experience_years=?, avg_closing_days=? WHERE Agent_ID=?
                    """, (name, phone, email, commission_rate, deals_closed, rating, exp_years, avg_closing_days, agent_id)
                    )

                    conn.commit()
                    st.success("Agent record has been updated successfully")
                    st.rerun()

    if selected_table == "Agents" and operation == "Delete":
        st.text("Delete Agent:")

        agents = pd.read_sql("SELECT Agent_ID FROM agents", conn)
        agent_id = st.selectbox(
            "Select Agent",
            agents,
            index=None,
            placeholder="Select",
            width=200
        )

        if agent_id:
            agentinfo = pd.read_sql("SELECT * FROM agents WHERE Agent_ID=?", conn, params=(agent_id,))
            st.dataframe(agentinfo, hide_index=True)

            confirm = st.checkbox("Are you sure, you want to delete this record")

            delete = st.button("Delete Agent", type="primary")

            if delete:
                if not confirm:
                    st.error("Please confirm the checkbox to delete this record")
                else:
                    cursor.execute(
                        """
                    DELETE FROM agents WHERE Agent_ID=?
                    """, (agent_id,)
                    )

                    conn.commit()
                    st.success("Agent record has been deleted successfully")
                    st.rerun()

    # Buyers Crud Operations
    if selected_table == "Buyers" and operation == "View":
        st.text("Buyers View:")
        crud_list = run_query("SELECT * FROM buyers")
        st.dataframe(crud_list, hide_index=True)
    
    if selected_table == "Buyers" and operation == "Add":
        st.text("Add Buyer:")

        with st.form("add_buyer_form"):
            col1, col2, col3 = st.columns(3)

            buyers          = pd.read_sql("SELECT Count(*) AS RowNo FROM buyers", conn)
            buyerid         = buyers.iloc[0]["RowNo"]+1
            sales           = pd.read_sql("SELECT Sale_ID FROM sales", conn)
            buyertypes      = pd.read_sql("SELECT buyer_type FROM buyers GROUP BY buyer_type", conn)
            paymentModes    = pd.read_sql("SELECT payment_mode FROM buyers GROUP BY payment_mode", conn)

            with col1:
                bid = st.text_input("Buyer Id", value=buyerid, disabled=True)
                saleid = st.selectbox("Sale_ID", sales, index=None, placeholder="Select")
                buyer_type = st.selectbox("Buyer Type", buyertypes, index=None, placeholder="Select")
                
            with col2:
                payment_mode = st.selectbox("Payment Mode", paymentModes, index=None, placeholder="Select")
                loan_taken= st.selectbox("Loan Taken", [True, False])

            with col3:
                loan_provider = st.text_input("Loan Provider")
                loan_amount = st.number_input("Loan Amount")

            submit = st.form_submit_button("Submit", type="primary")

            if submit:
                cursor.execute("""INSERT INTO buyers(buyer_id, sale_id, buyer_type, payment_mode, loan_taken, loan_provider, loan_amount) VALUES(?, ?, ?, ?, ?, ?, ?)
                    """, (bid, saleid, buyer_type, payment_mode, loan_taken, loan_provider, loan_amount))

                conn.commit()
                st.success("New buyer record added successfully")
                st.rerun()

    if selected_table == "Buyers" and operation == "Update":
        st.text("Update Buyer:")    

        buyers      = pd.read_sql("SELECT buyer_id FROM buyers", conn)
        buyer_id    = st.selectbox(
            "Select Buyer",
            buyers,
            index=None,
            placeholder="Select",
            width=200
        )

        if buyer_id:
            buyerinfo = pd.read_sql("SELECT * FROM buyers WHERE buyer_id=?", conn, params=(buyer_id,))

            with st.form("update_buyer_form"):
                col1, col2, col3 = st.columns(3)

                buyers          = pd.read_sql("SELECT Count(*) AS RowNo FROM buyers", conn)

                sales           = pd.read_sql("SELECT Sale_ID FROM sales", conn)
                sales_list      = sales["Sale_ID"].tolist()
                current_sale_id = buyerinfo.iloc[0]["sale_id"]
                saleid_index    = sales_list.index(current_sale_id)

                buyertypes      = pd.read_sql("SELECT buyer_type FROM buyers GROUP BY buyer_type", conn)
                buyertypes_list = buyertypes["buyer_type"].tolist()
                current_btype_id= buyerinfo.iloc[0]["buyer_type"]
                btype_index     = buyertypes_list.index(current_btype_id)

                paymentModes    = pd.read_sql("SELECT payment_mode FROM buyers GROUP BY payment_mode", conn)
                pmlist          = paymentModes["payment_mode"].tolist()
                pm_index        = pmlist.index(buyerinfo.iloc[0]['payment_mode'])

                loan_index = 0 if buyerinfo.iloc[0]["loan_taken"] == 1 else 1
            
                with col1:
                    bid = st.text_input("Buyer Id", value=buyer_id, disabled=True)
                    saleid = st.selectbox("Sale_ID", sales, index=saleid_index, placeholder="Select")
                    buyer_type = st.selectbox("Buyer Type", buyertypes, index=btype_index, placeholder="Select")

                with col2:
                    payment_mode = st.selectbox("Payment Mode", paymentModes, index=pm_index, placeholder="Select")
                    loan_taken= st.selectbox("Loan Taken", [True, False], index=loan_index)
                
                with col3:
                    loan_provider = st.text_input("Loan Provider", value=buyerinfo.iloc[0]["loan_provider"])
                    loan_amount = st.number_input("Loan Amount", value=buyerinfo.iloc[0]["loan_amount"])
                
                update = st.form_submit_button("Update", type="primary")

                if update:
                    cursor.execute(
                        """
                        UPDATE buyers SET sale_id=?, buyer_type=?, payment_mode=?, loan_taken=?, loan_provider=?, loan_amount=? WHERE buyer_id=?
                        """, (saleid, buyer_type, payment_mode, loan_taken, loan_provider, loan_amount, bid)
                    )

                    conn.commit()
                    st.success("Buyer record has been updated successfully")
                    st.rerun()

    if selected_table == "Buyers" and operation == "Delete" :
        st.text("Delete Buyer:") 

        buyers      = pd.read_sql("SELECT buyer_id FROM buyers", conn)

        buyer_id    = st.selectbox(
            "Select Buyer",
            buyers,
            index=None,
            placeholder="Select",
            width=200
        )
        
        if buyer_id:
            buyerinfo = pd.read_sql("SELECT * FROM buyers WHERE buyer_id=?", conn, params=(buyer_id,))

            st.dataframe(buyerinfo, hide_index=True)

            confirm = st.checkbox("Are you sure, you want to delete this record")
            
            delete = st.button("Delete", type="primary")
            
            if delete:
                if not confirm:
                    st.error("Please confirm the checkbox to delete this record")
                else:
                    cursor.execute(
                        """
                        DELETE FROM buyers WHERE buyer_id=?
                        """, (buyer_id,)
                    )
            
                    conn.commit()
                    st.success("Buyer record has been deleted successfully")
                    st.rerun()

    ####################################### 
    # PROPERTY ATTRIBUTES CRUD OPREATIONS #    
    ####################################### 

    if selected_table == "Property Attributes" and operation == "View" :
        st.text("Property attribute list:")
        crud_list = run_query("SELECT * FROM property_attributes")
        st.dataframe(crud_list, hide_index=True)

    if selected_table == "Property Attributes" and operation == "Add":
        st.text("Add Property Attribute")

        with st.form("add_property_attribute_form"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                attrs_res   = pd.read_sql("SELECT Count(*) AS RowNo FROM property_attributes", conn)
                attr_id     = attrs_res.iloc[0]["RowNo"]+1
                attrid      = st.number_input("Attribute Id", value=attr_id, disabled=True)

                listings    = pd.read_sql("SELECT Listing_ID FROM listings", conn)            
                listing_id  = st.selectbox("Listing ID", listings)   

                bedrooms    = st.number_input("Bedrooms")
                bathrooms   = st.number_input("Bathrooms")

            with col2:
                floor_number    = st.number_input("Floor number")
                total_floors    = st.number_input("Total Floors")
                year_built      = st.number_input("Year Build")
                
            with col3:
                is_rented           = st.selectbox("Is Rented", [True, False])
                tenant_count        = st.number_input("Tenant Count")
                furnishing_status   = pd.read_sql("SELECT furnishing_status FROM property_attributes GROUP BY furnishing_status", conn)
                furnishing_status   = st.selectbox("Furnishing Status", furnishing_status)

            with col4:
                metro_distance_km   = st.number_input("Metro Distance KM")
                parking_available   = st.selectbox("Parking Available", [True, False])
                power_backup        = st.selectbox("Power Backup", [True, False])

            submit = st.form_submit_button("Submit", type="primary")

            if submit:
                cursor.execute(
                    """
                    INSERT INTO property_attributes(attribute_id, listing_id, bedrooms, bathrooms, floor_number, total_floors, year_built, is_rented, tenant_count, furnishing_status, metro_distance_km, parking_available, power_backup) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (attrid, listing_id, bedrooms, bathrooms, floor_number, total_floors, year_built, is_rented, tenant_count, furnishing_status, metro_distance_km, parking_available, power_backup)
                )

                conn.commit()
                st.success("New record has been added successfully")
                st.rerun()

    if selected_table == "Property Attributes" and operation == "Update":
        st.text("Update Property Attributes:")    
    
        properties_attrs = pd.read_sql("SELECT buyer_id FROM buyers", conn)
        pa_id = st.selectbox(
            "Select Property Attribute",
            properties_attrs,
            index=None,
            placeholder="Select",
            width=200
        )
    
        if pa_id:
            painfo = pd.read_sql("SELECT * FROM property_attributes WHERE attribute_id=?", conn, params=(pa_id,))
    
            with st.form("update_pa_form"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    attrs_res   = pd.read_sql("SELECT Count(*) AS RowNo FROM property_attributes", conn)
                    attr_id     = attrs_res.iloc[0]["RowNo"]+1
                    attrid      = st.number_input("Attribute Id", value=attr_id, disabled=True)
                
                    listings    = pd.read_sql("SELECT Listing_ID FROM listings", conn)  
                    listings_list = listings["Listing_ID"].tolist()          
                    listing_index = listings_list.index(painfo.iloc[0]["listing_id"])

                    listing_id  = st.selectbox("Listing ID", listings, index=listing_index)   
                
                    bedrooms    = st.number_input("Bedrooms", value=painfo.iloc[0]["bedrooms"])
                    bathrooms   = st.number_input("Bathrooms", value=painfo.iloc[0]["bathrooms"])
                
                with col2:
                    floor_number    = st.number_input("Floor number", value=painfo.iloc[0]["floor_number"])
                    total_floors    = st.number_input("Total Floors", value=painfo.iloc[0]["total_floors"])
                    year_built      = st.number_input("Year Build", value=painfo.iloc[0]["year_built"])
                                
                with col3:
                    is_rented_index = 0 if painfo.iloc[0]["power_backup"] == 1 else 1
                    is_rented = st.selectbox("Is Rented", [True, False], index=is_rented_index)
                    tenant_count = st.number_input("Tenant Count", value=painfo.iloc[0]["tenant_count"])
                    furnishing_status = pd.read_sql("SELECT furnishing_status FROM property_attributes GROUP BY furnishing_status", conn)
                    furnishing_status   = st.selectbox("Furnishing Status", furnishing_status)
                
                with col4:
                    metro_distance_km = st.number_input("Metro Distance KM", value=painfo.iloc[0]["metro_distance_km"])
                    parking_index = 0 if painfo.iloc[0]["parking_available"] == 1 else 1                
                    parking_available = st.selectbox("Parking Available", [True, False], index=parking_index)
                    power_backup_index = 0 if painfo.iloc[0]["power_backup"] == 1 else 1
                    power_backup = st.selectbox("Power Backup", [True, False], index=power_backup_index)
                
                update = st.form_submit_button("Update", type="primary")

                if update:
                    cursor.execute(
                        """
                    UPDATE property_attributes SET listing_id=?, bedrooms=?, bathrooms=?, floor_number=?, total_floors=?, year_built=?, is_rented=?, tenant_count=?, furnishing_status=?, metro_distance_km=?, parking_available=?, power_backup=? WHERE attribute_id=?
                    """, (listing_id, bedrooms, bathrooms, floor_number, total_floors, year_built, is_rented, tenant_count, furnishing_status, metro_distance_km, parking_available, power_backup, pa_id)
                    )

                    conn.commit()
                    st.success("Record has been updated successfully")
                    st.rerun()

    if selected_table == "Property Attributes" and operation == "Delete" :
        st.text("Delete Property Attribute:") 
    
        property_attributes = pd.read_sql("SELECT attribute_id FROM property_attributes", conn)
    
        attribute_id = st.selectbox(
            "Select Property Attribute",
            property_attributes,
            index=None,
            placeholder="Select",
            width=200
        )
            
        if attribute_id:
            painfo = pd.read_sql("SELECT * FROM property_attributes WHERE attribute_id=?", conn, params=(attribute_id,))
    
            st.dataframe(painfo, hide_index=True)
    
            confirm = st.checkbox("Are you sure, you want to delete this record")
                
            delete = st.button("Delete", type="primary")
                
            if delete:
                if not confirm:
                    st.error("Please confirm the checkbox to delete this record")
                else:
                    cursor.execute(
                        """
                        DELETE FROM property_attributes WHERE attribute_id=?
                        """, (attribute_id,)
                    )
                
                    conn.commit()
                    st.success("Buyer record has been deleted successfully")
                    st.rerun()


#######################
##### SQL QUERIES #####
#######################

elif menu == "SQL Queries":
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView Analytics Dashboard"
        
    st.markdown(
        """
        <style>
            .re-title{
                text-align:center;
                margin-bottom:15px;
            }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
        """, unsafe_allow_html=True
    )
        
    st.subheader("SQL Queries")
    # st.subheader("Listings")

    queries = {
        "1. Total Listings by City":
        """
        SELECT City,
            COUNT(*) AS TotalListings
        FROM listings
        GROUP BY City
        ORDER BY TotalListings DESC
        """,

        "2. Average Property Price by City":
        """
        SELECT City,
            ROUND(AVG(Price),2) AS AveragePrice
        FROM listings
        GROUP BY City
        ORDER BY AveragePrice DESC
        """,

        "3. Top 10 Most Expensive Properties":
        """
        SELECT Listing_ID,
            City,
            Property_Type,
            Price
        FROM listings
        ORDER BY Price DESC
        LIMIT 10
        """,

        "4. Do properties closer to metro stations command higher prices?":
        """
            SELECT
                CASE
                    WHEN PA.metro_distance_km < 2 THEN '0-2 KM'
                    WHEN PA.metro_distance_km < 5 THEN '2-5 KM'
                    WHEN PA.metro_distance_km < 10 THEN '5-10 KM'
                    ELSE '10+ KM'
                END AS Metro_Distance,
                CAST(AVG(L.Price) AS INTEGER) AS Average_Price,
                COUNT(*) AS Total_Properties
            FROM listings L
            JOIN property_attributes PA
            ON L.Listing_ID = PA.listing_id
            GROUP BY Metro_Distance
            ORDER BY Average_Price;
        """,

        "5. Are rented properties priced differently from non-rented ones?":
        """
        SELECT
            CASE
                WHEN PA.is_rented = 1 THEN 'Rented'
                ELSE 'Non Rented'
            END AS RentalType,

            CAST(AVG(L.Price) AS INTEGER) AS Average_Price,
            COUNT(*) AS Total_Properties

        FROM listings L
        LEFT JOIN property_attributes PA
        ON L.Listing_ID = PA.listing_id

        GROUP BY RentalType""",

        "6. How do bedrooms and bathrooms affect pricing?":
        """
            SELECT
                PA.bedrooms,
                PA.bathrooms,
                CAST(AVG(L.Price) AS INTEGER) AS AveragePrice,
                COUNT(*) AS TotalProperties
            FROM listings L
            JOIN property_attributes PA
                ON L.Listing_ID = PA.listing_id
            GROUP BY
                PA.bedrooms,
                PA.bathrooms
            ORDER BY
                PA.bedrooms,
                PA.bathrooms;
        """,

        "7. Do properties with parking and power backup sell at higher prices?":
        """
            SELECT 
                CASE 
                    WHEN PA.parking_available = 1 THEN 'Yes'
                    ELSE 'No'
                END AS Parking,
        
                CASE 
                    WHEN PA.power_backup = 1 THEN 'Yes'
                    ELSE 'No'
                END AS Power_Backup,
                CAST(AVG(L.Price) AS INTEGER) AS AveragePrice,
                count(*) AS TotalProperties
            FROM listings L
            LEFT JOIN property_attributes PA
            ON L.Listing_ID=PA.listing_id
            GROUP BY Parking, Power_Backup
            ORDER BY AveragePrice DESC
        """,

        "8. How does year built influence listing price?":
        """
        SELECT PA.year_built AS BuiltYear, CAST(AVG(Price) AS INTEGER) AS AveragePrice, COUNT(*) AS TotalProperties
        FROM listings L
        JOIN property_attributes PA
        ON L.Listing_ID=PA.listing_id
        GROUP BY BuiltYear
        ORDER BY BuiltYear DESC
        """,

        "9. Which cities have the highest average property prices?":
        """SELECT avg(Price) as AveragePrice, City FROM listings GROUP BY City ORDER BY AveragePrice DESC LIMIT 1""",

        "10. How are properties distributed across price buckets?":
        """
        SELECT
            CASE
                WHEN Price < 500000 THEN 'Budget'
                WHEN Price BETWEEN 500000 AND 1000000 THEN 'Affordable'
                WHEN Price BETWEEN 1000001 AND 2000000 THEN 'Mid-Range'
                WHEN Price BETWEEN 2000001 AND 3000000 THEN 'Premium'
                WHEN Price BETWEEN 3000001 AND 4000000 THEN 'Luxury'
                ELSE 'Ultra Luxury'
            END AS PriceBucket,

            COUNT(*) AS TotalProperties,
            CAST(AVG(Price) AS INTEGER) AS AveragePrice

        FROM listings

        GROUP BY PriceBucket

        ORDER BY AveragePrice;
        """,

        "11. What is the average days on market by city?":
        """
        SELECT L.City, CAST(AVG(S.Days_on_Market) AS INTEGER) AS DaysOnMarket 
        FROM listings L JOIN sales S ON L.Listing_ID=S.listing_id
        GROUP BY L.City
        ORDER BY DaysOnMarket DESC
        """,

        "12. Which property types sell the fastest?":
        """
        SELECT
            L.Property_Type,
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysToSell,
            COUNT(*) AS TotalSales
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID = S.Listing_ID
        GROUP BY L.Property_Type
        ORDER BY AverageDaysToSell ASC
        """,

        "13. What percentage of properties are sold above listing price?":
        """
        SELECT
            COUNT(*) AS TotalSoldProperties,
        
            SUM(
                CASE
                    WHEN S.Sale_Price > L.Price THEN 1
                    ELSE 0
                END
            ) AS SoldAboveListing,
        
            ROUND(
                SUM(
                    CASE
                        WHEN S.Sale_Price > L.Price THEN 1
                        ELSE 0
                    END
                ) * 100.0 / COUNT(*),
                2
            ) AS PercentageSoldAboveListing
        
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID = S.Listing_ID
        """,
        "14. What is the sale-to-list price ratio by city?":
        """
        SELECT
            L.City,
            ROUND(AVG((S.Sale_Price * 100.0) / L.Price), 2) AS SaleToListPriceRatio,
            COUNT(*) AS TotalSales
        FROM listings L
        INNER JOIN sales S
            ON L.Listing_ID = S.Listing_ID
        GROUP BY L.City
        ORDER BY SaleToListPriceRatio DESC
        """,

        "15. Which listings took more than 90 days to sell?":
        """
        SELECT 
            L.Listing_ID, 
            L.City,
            L.Property_Type,
            L.Price,
            S.Sale_Price,
            S.Days_on_Market
        FROM 
            listings L 
        LEFT JOIN sales S 
        ON L.Listing_ID=S.listing_id 
        WHERE 
            S.Days_on_Market>90 
        ORDER BY S.Days_on_Market DESC
        """,

        "16. How does metro distance affect time on market?":
        """
        SELECT
            PA.metro_distance_km,
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysOnMarket,
            COUNT(*) AS TotalProperties
        FROM property_attributes PA
        INNER JOIN sales S
            ON PA.listing_id = S.Listing_ID
        GROUP BY PA.metro_distance_km
        ORDER BY PA.metro_distance_km ASC
        """,

        "17. What is the monthly sales trend?":
        """
        SELECT
            strftime('%Y-%m', Date_Sold) AS SaleMonth,
            COUNT(*) AS TotalSales
        FROM sales
        GROUP BY SaleMonth
        ORDER BY SaleMonth
        """,

        "18. Which properties are currently unsold?":
        """
        SELECT 
            L.* 
        FROM listings L
        INNER JOIN sales S
        ON L.Listing_ID=S.Listing_ID
        """,

        "19. Which agents have closed the most sales?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            count(S.Listing_ID) as MostSales
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name 
        ORDER BY MostSales DESC
        """,

        "20. Who are the top agents by total sales revenue?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            sum(S.Sale_Price) as TotalSalesRevenue
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name
        ORDER BY TotalSalesRevenue DESC
        """,

        "21. Which agents close deals fastest?":
        """
        SELECT 
            A.Agent_ID,
            A.Name,
            CAST(AVG(S.Days_on_Market) AS INTEGER) as FewerDays
        FROM sales S
        INNER JOIN listings L ON S.Listing_ID=L.Listing_ID
        INNER JOIN agents A ON L.Agent_ID=A.Agent_ID
        GROUP BY A.Agent_ID, A.Name
        ORDER BY FewerDays ASC
        """,

        "22. Does experience correlate with deals closed?":
        """
        SELECT
            experience_years,
            CAST(AVG(deals_closed) AS INTEGER) AS AverageDealsClosed,
            COUNT(*) AS TotalAgents
        FROM agents
        GROUP BY experience_years
        ORDER BY experience_years
        """,

        "23. Do agents with higher ratings close deals faster?":
        """
        SELECT 
            rating,
            CAST(AVG(deals_closed) AS INTEGER) AS AverageDealsClosed,
            COUNT(*) AS TotalAgents
        FROM 
            agents
        GROUP BY rating
        ORDER BY rating
        """,

        "24. What is the average commission earned by each agent?":
        """
        SELECT
            A.Agent_ID,
            A.Name,
            CAST(AVG((S.Sale_Price * A.commission_rate) / 100) AS INTEGER) AS AverageCommissionEarned
        FROM sales S
        INNER JOIN listings L
            ON S.Listing_ID = L.Listing_ID
        INNER JOIN agents A
            ON L.Agent_ID = A.Agent_ID
        GROUP BY
            A.Agent_ID,
            A.Name
        ORDER BY
            AverageCommissionEarned DESC;
        """,

        "25. Which agents currently have the most active listings?":
        """
        SELECT
            A.Agent_ID,
            A.Name,
            COUNT(L.Listing_ID) AS ActiveListings
        FROM listings L
        INNER JOIN agents A
            ON L.Agent_ID = A.Agent_ID
        LEFT JOIN sales S
            ON L.Listing_ID = S.Listing_ID
        WHERE S.Listing_ID IS NULL
        GROUP BY
            A.Agent_ID,
            A.Name
        ORDER BY
            ActiveListings DESC;
        """,

        "26. What percentage of buyers are investors vs end users?":
        """
        SELECT 
            buyer_type,
            COUNT(*) AS TotalBuyers,
            ROUND(
                (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM buyers), 2
            ) AS Percentage     
        FROM 
            buyers
        GROUP BY 
            buyer_type
        """,

        "27. Which cities have the highest loan uptake rate?":
        """
        SELECT 
            L.City,
            COUNT(B.buyer_id) AS TotalBuyers,
            SUM(
                CASE 
                    WHEN B.loan_taken = 1 THEN 1 ELSE 0
                END
            ) AS LoanBuyers,
            ROUND(
                SUM(
                    CASE 
                        WHEN B.loan_taken = 1 THEN 1 ELSE 0
                    END
                ) * 100.0 / COUNT(B.buyer_id), 2
            ) AS HighestLoanUptake
        FROM listings L 
        LEFT JOIN buyers B ON L.Listing_ID=B.sale_id
        GROUP BY L.City
        ORDER BY HighestLoanUptake DESC
        """,

        "28. What is the average loan amount by buyer type?":
        """
        SELECT 
            CAST(AVG(loan_amount) AS INTEGER) AS AverageLoanAmount,
            buyer_type
        FROM 
            buyers
        WHERE loan_taken=1
        GROUP BY buyer_type
        ORDER BY AverageLoanAmount DESC
        """,

        "29. Which payment mode is most commonly used?":
        """
        SELECT 
            payment_mode,
            count(buyer_id) as TotalTransactions 
        FROM 
            buyers 
        GROUP BY payment_mode
        ORDER BY TotalTransactions DESC
        """,

        "30. Do loan-backed purchases take longer to close?":
        """
        SELECT
            CASE
                WHEN B.loan_taken = 1 THEN 'Loan'
                ELSE 'No Loan'
            END AS LoanStatus,
        
            CAST(AVG(S.Days_on_Market) AS INTEGER) AS AverageDaysToClose,
        
            COUNT(*) AS TotalPurchases
        
        FROM buyers B
        INNER JOIN sales S
        ON B.sale_id = S.Listing_ID
        
        GROUP BY LoanStatus
        ORDER BY AverageDaysToClose DESC
        """        

    }

    selected_query = st.selectbox(
        "Select SQL Query",
        list(queries.keys())
    )

    if selected_query:
        df = pd.read_sql(
            queries[selected_query],
            conn
        )

        st.text(selected_query)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
else:
    st.title="BrickView Dasboard"
    st.write="Welcome to BrickView Analytics Dashboard"
    
    st.markdown(
            """
        <style>
        div[data-testid="stMarkdownContainer"]{
            margin-bottom:30px!important;
        }
        .stMain{
            background:#060!important;
        }
        .re-title{
            text-align:center;
            margin-bottom:15px;
        }
        </style>
        <div class="re-title">
            <h1>🏠</h1>
            <h3>BrickView Real Estate</h3>
        </div>
        """, unsafe_allow_html=True
        )
    
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
    
    st.subheader("Introduction")
    st.subheader("Listings")
    st.dataframe(listings)