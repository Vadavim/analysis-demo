import streamlit as st
from jsr.streamlit_components.components_general import component_time_picker, get_dataframes
from jsr.utils.col_namespace import *
from jsr.streamlit_components.components_operator import create_operator_freq_table, create_timeline_chart
import polars as pl

st.title("Operator Timeline")

dataframes = get_dataframes()
df_transactions = dataframes["transactions"]



# For ordering top and bottom components
top_container = st.container()
middle_container = st.container()
bottom_container = st.container()

# Create date selection component
with top_container:
    col1, col2 = top_container.columns(2)

# Col 1 -> Date Picker
with col1:
    tmin = df_transactions[Trans.START_TIME].min()
    tmax = df_transactions[Trans.START_TIME].max()
    selected_date = component_time_picker(tmin, tmax)

    # Filter dataframe to only show events that day
    filtered_df = (
        df_transactions
        .filter(pl.col(Trans.START_TIME).dt.day() == selected_date.day)
        .filter(pl.col(Trans.START_TIME).dt.month() == selected_date.month)
        .sort("OPERATOR_ID")
    )

    # Need to create a Y-axis category filter (for timeline chart)
    all_operators = filtered_df[Trans.OPERATOR_ID].unique().to_list()
    operators_with_shifts = filtered_df[Trans.OPERATOR_ID].unique()
    df_for_plot = filtered_df.filter(
        pl.col(Trans.OPERATOR_ID).is_in(operators_with_shifts)
    )
    sorted_operators = filtered_df[Trans.OPERATOR_ID].unique().sort().to_list()

# Col 2 -> Category Picker
with col2:
    color_filter = st.selectbox(
        "Select what to color timelines with",
        ["Shift ID", "Transaction Type", "Transaction Qty"],
    )
    remap_dict = {"Shift ID": Trans.FEAT_SHIFT_ID,
                  "Transaction Type": Trans.TRANSACTION_TYPE,
                  "Transaction Qty": Trans.TRANSACTION_QTY}
    color_filter = remap_dict[color_filter]


# Bottom Container -> selectable list of operator IDs to filter DF with
with bottom_container:
    options = st.multiselect(
        "Operator IDs",
        sorted_operators,
        default=sorted_operators
    )
    filtered_df = (
        filtered_df.filter(
            pl.col(Trans.OPERATOR_ID).is_in(options)
        )
    )
    sorted_operators = filtered_df[Trans.OPERATOR_ID].unique().sort().to_list()

# Tabs
with middle_container:
    tab_timeline, tab_df = st.tabs(["Timeline", "Dataframe"])
    with tab_timeline:
        create_timeline_chart(filtered_df, sorted_operators,
                              selected_date, color_filter)
    with tab_df:
        st.dataframe(filtered_df)



