import streamlit as st
import pandas
import os

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 
    """
)

st.markdown(os.getcwd())

# df = pandas.read_csv("data/SHIFT_SCHEDULE.csv")
# df = pandas.read_csv("data/WAREHOUSE_SHIPMENTS.csv")
df = pandas.read_csv("data/WAREHOUSE_TRANSACTIONS.csv")
st.table(df)

