from typing import Optional

import streamlit as st
import pandas
import os
import polars as pl
from jsr.utils.processing import process_dataframes, create_freq_map
from jsr.utils.col_namespace import *
import plotly.express as px
from datetime import datetime


def create_shipment_value_summary(df_shipments: pl.DataFrame, summary_type: str, category: Optional[str] = None):
    if summary_type == "Shipment Count":
        exp_agg = pl.col(Ship.VALUE).count()
    elif summary_type == "Shipment Mean Value":
        exp_agg = pl.col(Ship.VALUE).mean()
    elif summary_type == "Shipment Max Value":
        exp_agg = pl.col(Ship.VALUE).max()
    else:
        exp_agg = pl.col(Ship.VALUE).sum()

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


