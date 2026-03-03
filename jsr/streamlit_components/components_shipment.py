from typing import Optional, Tuple

import streamlit as st
import polars as pl
from jsr.utils.col_namespace import *
import plotly.express as px

def create_shipment_value_summary(df_shipments: pl.DataFrame, summary_type: str,
                                  category: Optional[str] = None) -> Tuple[st.plotly_chart, pl.DataFrame]:
    """ Creates a summary of shipments over each day based on options selected.
    Args:
        df_shipments: Shipments dataframe
        summary_type: (str) Determines type of summary done over each day:
            Shipment Count -> number of shipments made during that day
            Shipment Mean Value -> average value of shipments during that day
            Shipment Max Value -> maximum value of shipments during that day
            Else -> total value of shipments during that day
        category:
            "All Shipments" -> aggregates shipments together into single summary
            "Order Line ID" -> show breakdown of shipment summary by Order Line ID

    Returns:
        Chart of transaction summaries (st.plotly_chart)
        Filtered view of polars dataframe (pl.DataFrame)
    """
    if summary_type == "Shipment Count":
        exp_agg = pl.col(Ship.VALUE).count()
    elif summary_type == "Shipment Mean Value":
        exp_agg = pl.col(Ship.VALUE).mean()
    elif summary_type == "Shipment Max Value":
        exp_agg = pl.col(Ship.VALUE).max()
    else:
        exp_agg = pl.col(Ship.VALUE).sum()


    # Create summary of shipments over each day
    # Type of summary depends on summart_type argument
    value_summary_by_day = (
        df_shipments
        .sort(Ship.SHIP_DATE)
        .group_by_dynamic(
            index_column=Ship.SHIP_DATE,
            every="1d",
            group_by=category
        )
        .agg(value=exp_agg)
    )

    # Create Fig
    fig = px.line(value_summary_by_day, x=Ship.SHIP_DATE, y="value",
                  color=category)
    fig.update_yaxes(title_text=summary_type)
    fig.update_xaxes(title_text="Date")
    return st.plotly_chart(fig), value_summary_by_day


