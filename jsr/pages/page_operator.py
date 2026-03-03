import streamlit as st

from jsr.streamlit_components.components_general import get_dataframes
from jsr.utils.col_namespace import *
from jsr.streamlit_components.components_operator import create_operator_freq_table
import polars as pl
from datetime import datetime, timedelta

st.title("Transaction Summary by Operator")
st.markdown("""
**Note**: this interface was not fully developed. The intent was to try to create breakdowns by operator ID on stats
such as transaction count, duration, and gaps (between transactions) over a certain time period. However, ran out of time...
""")

dataframes = get_dataframes()
df_transactions = dataframes["transactions"]

tmin = df_transactions[Trans.START_TIME].min()
tmax = df_transactions[Trans.START_TIME].max()
selected_range = st.slider(
    "Select date range (drag handles or click to move)",
    min_value=tmin,
    max_value=tmax,
    value=(tmin, tmax),
    step=timedelta(days=1),
    format="MMM DD, YYYY"
)

start_date, end_date = selected_range

# Add components
filtered_df = (
    df_transactions
    .filter(
        pl.col(Trans.START_TIME) >= start_date,
        pl.col(Trans.START_TIME) <= end_date,
    )
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(
        label="Transaction Count",
        value= len(filtered_df)
    )

create_operator_freq_table(df_transactions, start_date, end_date)


