from datetime import datetime
from typing import Optional

import plotly.express as px
import polars as pl
import streamlit as st

from jsr.utils.col_namespace import *
from jsr.utils.processing import create_freq_map


def create_transaction_summary_by_shift(df_transactions: pl.DataFrame,
                                        summary_type: str,
                                        filter_category: Optional[str] = None):
    # Summarize based on summary type
    if summary_type == "# of Transactions":
        exp_summary = pl.col(Trans.FEAT_SHIFT_ID).count().alias("transaction_count")
    else:
        exp_summary = pl.col(Trans.OPERATOR_ID).unique().count().alias("operator_count")

    summary_df = df_transactions

    # Apply filters
    if filter_category != "All Transactions":
        print("Here")
        summary_df = (
            df_transactions
            .filter(pl.col(Trans.TRANSACTION_TYPE) == filter_category)
        )

    # Perform summary
    summary_df = (
        summary_df
        .group_by(Trans.FEAT_SHIFT_START)
        .agg(summary = exp_summary,
             SHIFT_ID = pl.col(Trans.FEAT_SHIFT_ID).first())
        .with_columns(day=pl.col(Trans.FEAT_SHIFT_START).dt.strftime("%a"))
    ).sort(Trans.FEAT_SHIFT_ID)

    # Plot
    fig = px.bar(summary_df, x="SHIFT_START", y="summary", color=Trans.FEAT_SHIFT_ID,
                 text=Trans.FEAT_SHIFT_ID, hover_name="day")

    fig.update_yaxes(title_text=summary_type)
    fig.update_xaxes(title_text="Shift Start")
    fig.update_layout(height=350)
    return st.plotly_chart(fig), summary_df


def create_timeline_chart(df_transactions: pl.DataFrame,
                          sorted_operators, selected_date: datetime, color_filter: str):
    fig = px.timeline(df_transactions, x_start="START_TIME",
                      x_end="END_TIME", y="OPERATOR_ID", color=color_filter)
    fig.update_traces(width=0.7)
    fig.update_layout(bargap=0.01, bargroupgap=0.0)
    fig.update_yaxes(
        type="category",
        dtick=1,
        tickfont_size=10,
        categoryorder="array",
        categoryarray=sorted_operators,
        title="OPERATOR_ID",
    )
    fig.update_layout(
        xaxis_title="Time", xaxis_title_font_size=14,
        yaxis_title="Operator ID", yaxis_title_font_size=14,
        title="Timeline for {}".format(selected_date),
        title_y=0.99,
        title_font_size=20,
        font_family="Overpass",
        margin=dict(l=40, r=20, t=40, b=30),
    )
    fig.update_layout(bargap=0, barmode='overlay')

    # default_figure_settings(fig,
    #                         x_label="Time", y_label="Operator ID", title="Shift Breakdown")

    fig.add_vline(x=datetime(2020, selected_date.month, selected_date.day, 19), line_dash="dash", line_color="black", line_width=1)
    fig.add_vline(x=datetime(2020, selected_date.month, selected_date.day, 7), line_dash="dash", line_color="black", line_width=1)
    return st.plotly_chart(fig, theme=None)

def create_operator_freq_table(df_transactions: pl.DataFrame, date_min, date_max):
    df_transactions = (
        df_transactions
        .filter(pl.col(Trans.START_TIME) > date_min)
        .filter(pl.col(Trans.START_TIME) < date_max)
    )
    freq_map = create_freq_map(df_transactions).sort("OPERATOR_ID")
    component_df = st.dataframe(freq_map,
                 column_config={
                     "count" : st.column_config.LineChartColumn( "Transaction Count" ),
                     "mean_duration": st.column_config.BarChartColumn("Average Transaction Duration (seconds)"),
                     "mean_gap": st.column_config.BarChartColumn("Average Transaction Gap (seconds)")
                 })
    return component_df


