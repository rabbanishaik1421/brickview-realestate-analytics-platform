import streamlit as st

from database import get_connection
from utils import run_query
from common import page_header
from dashboard import show_dashboard
from filters import showfilter
from visualization import show_visualization
from crud_operations import show_crudoperations
from sql_queries import show_sqlqueries

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
conn = get_connection()
cursor = conn.cursor()

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

page_header()

# INTRODUCTION #
if menu == "Introduction":        
    show_dashboard()

# Filters & Explorer #
elif menu == "Filters & Explorer":
    showfilter()

# VISUALIZATION #
elif menu == "Visualization":
    show_visualization()

# Crud Operations #
elif menu == "Crud Operations":
    show_crudoperations()

# SQL QUERIES #
elif menu == "SQL Queries":
    show_sqlqueries()
    
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