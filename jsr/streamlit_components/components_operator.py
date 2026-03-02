import streamlit as st
import pandas
import os
import polars as pl
from jsr.utils.processing import process_dataframes, create_freq_map


def create_operator_freq_table(df_transactions: pl.DataFrame):
    freq_map = create_freq_map(df_transactions)
    st.dataframe(freq_map,
                 column_config={
                     "count" : st.column_config.LineChartColumn(
                         "Freq Map"
                     )
                 })
