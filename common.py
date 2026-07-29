import streamlit as st

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def page_header():

    st.markdown("""
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
    """,
    unsafe_allow_html=True)
    