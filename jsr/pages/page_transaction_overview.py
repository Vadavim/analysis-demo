import streamlit as st
from jsr.streamlit_components.components_general import component_time_picker, get_dataframes
from jsr.streamlit_components.components_operator import create_transaction_summary_by_shift
from jsr.utils.plotting import default_figure_settings
from jsr.utils.col_namespace import *
import polars as pl
from datetime import datetime, timedelta, date
import plotly.express as px


st.title("Transaction Overview")
dataframes = get_dataframes()
df_transactions = dataframes["transactions"]

top_container = st.container()
bottom_container = st.container()

with top_container:
    col1, col2, col3, col4 = st.columns(4)


# Col 1 -> Period Picker
with col1:
    period = st.selectbox("Period", ["Weekly", "Monthly", "Yearly"])
    td = {"Weekly": timedelta(days=7),
          "Monthly": timedelta(days=30),
          "Yearly": timedelta(days=365)}[period]

# Col 2 -> Date Picker
with col2:

    tmin = df_transactions[Trans.START_TIME].min()
    tmax = df_transactions[Trans.START_TIME].max()
    selected_date = component_time_picker(tmin, tmax)
    future_date = selected_date + td

    filtered_df = (
        df_transactions
        .filter(pl.col(Trans.FEAT_SHIFT_START).dt.date() >= selected_date)
        .filter(pl.col(Trans.FEAT_SHIFT_START).dt.date() <= future_date)
        .sort(Trans.FEAT_SHIFT_START)
    )


# Col 3 -> Category Picker
with col3:
    transaction_type = st.selectbox(
        "Choose transaction type",
        options=["All Transactions", "Case Pick",
                 "Replenishment", "Pallet Pick", "Putaway Pallet"]
    )
    # if transaction_type == "All Transactions":
    #     transaction_type = None

# Col 4 -> Summary Picker
with col4:
    summary_type = st.selectbox(
        "Choose summary type",
        options=["# of Transactions", "# of Operators"]
    )

with bottom_container:
    tab_chart, tab_df = st.tabs(["Chart", "Dataframe"])

with tab_chart:
    chart, dataframe = create_transaction_summary_by_shift(
        filtered_df, summary_type=summary_type,
        filter_category=transaction_type)
