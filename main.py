import streamlit as st

from database import get_connection
from utils import run_query
from common import page_header
from common import load_css
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

# def load_css():
#     with open("style.css") as f:
#         st.markdown(
#             f"<style>{f.read()}</style>",
#             unsafe_allow_html=True
#         )

# Loaded CSS
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
if menu == "Filters & Explorer":
    showfilter()

# VISUALIZATION #
if menu == "Visualization":
    show_visualization()

# Crud Operations #
if menu == "Crud Operations":
    show_crudoperations()

# SQL QUERIES #
if menu == "SQL Queries":
    show_sqlqueries()