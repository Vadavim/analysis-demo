import polars as pl
from polars import col
from polars import selectors as cs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import time
import numpy as np
from jsr.utils.processing import process_dataframes, _find_shift_ids
from jsr.utils.col_namespace import Sched, Ship, Trans
from plotly.subplots import make_subplots


def ship_plot_total_value_over_time(df_shipments: pl.DataFrame):

    # Extract Total values and mean time (for red hline)
    total_values_by_day = (
        df_shipments
        .sort(Ship.SHIP_DATE)
        .group_by_dynamic(Ship.SHIP_DATE, every="1d")
        .agg(total_value=col(Ship.VALUE).sum().alias("Total Value"))
    )
    mean_value = total_values_by_day["total_value"].mean()

    # Initial bar chart
    fig = px.bar(total_values_by_day, x=Ship.SHIP_DATE, y="total_value",
                 template="seaborn")
    fig.update_layout(
        xaxis_title="Day", xaxis_title_font_size=20,
        yaxis_title="Total", yaxis_title_font_size=20,
        title="Total Daily Value of Shipments", title_font_size=25
    )

    # Annotation - "Average" Box
    fig.add_annotation(
        xref="paper",
        x=1.12,
        y=mean_value,
        xanchor="right",
        text="Average",
        showarrow=False,
        ax=0,
        ay=-16,
        font=dict(size=14, color="red"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
    )

    # HLine - average value
    fig.add_hline(y=mean_value, line_dash="dash", line_color="red", line_width=2)

    return fig