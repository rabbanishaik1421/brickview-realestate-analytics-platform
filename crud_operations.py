import streamlit as st
from utils import run_query
from database import get_connection

def show_crudoperations():
    conn = get_connection()
    cursor = conn.cursor()

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

    # LISTINGS CRUD OPREATIONS #    
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

        listing = run_query("SELECT *FROM listings WHERE Listing_ID = ?", (selected_listing,))

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

        selected_list_df = run_query("SELECT *FROM listings WHERE Listing_ID=?", params=(selected_list,))

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

    # SALES CRUD OPREATIONS #    
    if selected_table == "Sales" and operation == "View":
        st.text("View Sales:")
        crud_list = run_query("SELECT * FROM sales")
        st.dataframe(crud_list)

    if selected_table == "Sales" and operation == "Add":
        st.text("Add Sale:")
        with st.form("add_sale_form"):
            
            col1, col2, col3, col4, col5 = st.columns(5)

            sales = run_query("SELECT COUNT(*) AS RowNo, MAX(Sale_ID) AS MaxSale FROM sales")
            rowno = sales.iloc[0]["RowNo"] + 1
            sale_id = f"S{rowno:05d}"

            listings = run_query("SELECT Listing_ID FROM listings")

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
        sales = run_query("SELECT Sale_ID FROM sales WHERE Sale_ID IS NOT NULL")
        sale_id = st.selectbox(
            "Select Sale ID",
            sales,
            index=None,
            placeholder="Choose a Sale ID",
            width=200
        )

        if sale_id:
            saleinfo = run_query("SELECT * FROM sales WHERE Sale_ID=?", (sale_id,))

            listings = run_query("SELECT Listing_ID FROM listings")

            with st.form("update_sale_form"):
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    listings = run_query(
                        "SELECT Listing_ID FROM listings ORDER BY Listing_ID",
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
        sales = run_query("SELECT * FROM sales")
        st.text("Delete Sale:")

        sale_id = st.selectbox(
            "Select Sale ID", 
            sales, 
            width=200,
            index=None,
            placeholder="Select Sale"
        )

        if sale_id:
            saleinfo = run_query("SELECT * FROM sales WHERE Sale_ID=?", (sale_id,))

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

            agents  = run_query("SELECT COUNT(*) AS RowNo FROM agents")
            rowno   = agents.iloc[0]["RowNo"] + 1
            # st.dataframe(rowno)
            agentid = f"A{rowno:04d}"

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

        agents = run_query("SELECT Agent_ID FROM agents")

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
            
                agentinfo = run_query("SELECT * FROM agents WHERE Agent_ID=?", (agent_id,))
            
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
                    # st.rerun()
                    st.success("Agent record has been updated successfully")

    if selected_table == "Agents" and operation == "Delete":
        st.text("Delete Agent:")

        agents = run_query("SELECT Agent_ID FROM agents")
        agent_id = st.selectbox(
            "Select Agent",
            agents,
            index=None,
            placeholder="Select",
            width=200
        )

        if agent_id:
            agentinfo = run_query("SELECT * FROM agents WHERE Agent_ID=?", (agent_id,))
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

            buyers          = run_query("SELECT Count(*) AS RowNo FROM buyers")
            buyerid         = buyers.iloc[0]["RowNo"]+1
            sales           = run_query("SELECT Sale_ID FROM sales")
            buyertypes      = run_query("SELECT buyer_type FROM buyers GROUP BY buyer_type")
            paymentModes    = run_query("SELECT payment_mode FROM buyers GROUP BY payment_mode")

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

        buyers      = run_query("SELECT buyer_id FROM buyers")
        buyer_id    = st.selectbox(
            "Select Buyer",
            buyers,
            index=None,
            placeholder="Select",
            width=200
        )

        if buyer_id:
            buyerinfo = run_query("SELECT * FROM buyers WHERE buyer_id=?", (buyer_id,))

            with st.form("update_buyer_form"):
                col1, col2, col3 = st.columns(3)

                buyers          = run_query("SELECT Count(*) AS RowNo FROM buyers")

                sales           = run_query("SELECT Sale_ID FROM sales")
                sales_list      = sales["Sale_ID"].tolist()
                current_sale_id = buyerinfo.iloc[0]["sale_id"]
                saleid_index    = sales_list.index(current_sale_id)

                buyertypes      = run_query("SELECT buyer_type FROM buyers GROUP BY buyer_type")
                buyertypes_list = buyertypes["buyer_type"].tolist()
                current_btype_id= buyerinfo.iloc[0]["buyer_type"]
                btype_index     = buyertypes_list.index(current_btype_id)

                paymentModes    = run_query("SELECT payment_mode FROM buyers GROUP BY payment_mode")
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

        buyers      = run_query("SELECT buyer_id FROM buyers")

        buyer_id    = st.selectbox(
            "Select Buyer",
            buyers,
            index=None,
            placeholder="Select",
            width=200
        )
        
        if buyer_id:
            buyerinfo = run_query("SELECT * FROM buyers WHERE buyer_id=?", (buyer_id,))

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

    # PROPERTY ATTRIBUTES CRUD OPREATIONS #    
    
    if selected_table == "Property Attributes" and operation == "View" :
        st.text("Property attribute list:")
        crud_list = run_query("SELECT * FROM property_attributes")
        st.dataframe(crud_list, hide_index=True)

    if selected_table == "Property Attributes" and operation == "Add":
        st.text("Add Property Attribute")

        with st.form("add_property_attribute_form"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                attrs_res   = run_query("SELECT Count(*) AS RowNo FROM property_attributes")
                attr_id     = attrs_res.iloc[0]["RowNo"]+1
                attrid      = st.number_input("Attribute Id", value=attr_id, disabled=True)

                listings    = run_query("SELECT Listing_ID FROM listings")            
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
                furnishing_status   = run_query("SELECT furnishing_status FROM property_attributes GROUP BY furnishing_status")
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
    
        properties_attrs = run_query("SELECT buyer_id FROM buyers")
        pa_id = st.selectbox(
            "Select Property Attribute",
            properties_attrs,
            index=None,
            placeholder="Select",
            width=200
        )
    
        if pa_id:
            painfo = run_query("SELECT * FROM property_attributes WHERE attribute_id=?", (pa_id,))
    
            with st.form("update_pa_form"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    attrs_res   = run_query("SELECT Count(*) AS RowNo FROM property_attributes")
                    attr_id     = attrs_res.iloc[0]["RowNo"]+1
                    attrid      = st.number_input("Attribute Id", value=attr_id, disabled=True)
                
                    listings        = run_query("SELECT Listing_ID FROM listings")  
                    listings_list   = listings["Listing_ID"].tolist()          
                    listing_index   = listings_list.index(painfo.iloc[0]["listing_id"])

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
                    furnishing_status = run_query("SELECT furnishing_status FROM property_attributes GROUP BY furnishing_status")
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
    
        property_attributes = run_query("SELECT attribute_id FROM property_attributes")
    
        attribute_id = st.selectbox(
            "Select Property Attribute",
            property_attributes,
            index=None,
            placeholder="Select",
            width=200
        )
            
        if attribute_id:
            painfo = run_query("SELECT * FROM property_attributes WHERE attribute_id=?", (attribute_id,))
    
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
