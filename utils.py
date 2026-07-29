import pandas as pd
from database import get_connection

def run_query(query, params=None):
    conn = get_connection()
    return pd.read_sql(query, conn, params=params)