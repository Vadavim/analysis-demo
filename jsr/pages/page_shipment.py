import streamlit as st

from jsr.streamlit_components.components_general import get_dataframes
from jsr.streamlit_components.components_shipment import create_shipment_value_summary
from jsr.utils.col_namespace import *
import polars as pl

st.title("Shipment Summary")

dataframes = get_dataframes() # persistent state
df_shipments = dataframes["shipments"]

top_container = st.container()
bottom_container = st.container()

# Col 1 -> Radio Buttons; Col 2 -> Plot
with top_container:
    col1, col2 = st.columns(2)
with col1:
    radio_summary = st.selectbox(
        "Choose a summary type",
        options=["Shipment Count", "Shipment Mean Value",
                 "Ship Total Value", "Shipment Max Value"]
    )

with col2:
    radio_category = st.selectbox(
        "Choose what to summarize over",
        options=["All Shipments", "Order Line ID"]
    )

remap_dict = {"All Shipments": None, "Order Line ID": Ship.ORDER_LINE_ID}
radio_category = remap_dict[radio_category]

# Chart and dataframe
with top_container:
    tab_chart, tab_df = st.tabs(["Chart", "Dataframe"])

# Filter multisect for ORDER_LINE_ID
with bottom_container:
    sorted_order_line_ids = df_shipments[Ship.ORDER_LINE_ID].unique().sort().to_list()
    options = st.multiselect(
        "Order Line IDs",
        sorted_order_line_ids,
        default=sorted_order_line_ids
    )
    filtered_df_shipments = (
        df_shipments
        .filter(pl.col(Ship.ORDER_LINE_ID).is_in(options))
    )

# Display tabs
with tab_chart:
    chart, value_summary_df = create_shipment_value_summary(filtered_df_shipments,
                                  summary_type=radio_summary,
                                  category=radio_category)
with tab_df:
    st.dataframe(value_summary_df)

