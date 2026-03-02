import streamlit as st
import pandas
import os
from jsr.utils.processing import process_dataframes, create_freq_map



dataframes = process_dataframes("data/")
df_schedule = dataframes["schedule"]
df_shipments = dataframes["shipments"]
df_transactions = dataframes["transactions"]

st.title("Test")
st.markdown(
    """ 
    This is a test
    """
)
# p = test_plot()
# st.plotly_chart(p)


