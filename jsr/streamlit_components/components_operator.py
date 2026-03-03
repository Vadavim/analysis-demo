from datetime import datetime
from typing import Optional, Tuple

import plotly.express as px
import polars as pl
import streamlit as st

from jsr.utils.col_namespace import *
from jsr.utils.processing import create_freq_map


def create_transaction_summary_by_shift(df_transactions: pl.DataFrame,
                                        summary_type: str,
                                        filter_category: Optional[str] = None) -> Tuple[st.plotly_chart, pl.DataFrame]:
    """ Creates a summary (by shift) of transactions. Filtered view of a px.bar chart
    Args:
        df_transactions: Transaction DataFrame
        summary_type: Type of summary (str) [transaction_count, operator_count]
        filter_category: Type of transaction to filter by

    Returns:
        Chart of transaction summaries (st.plotly_chart)
        Filtered view of polars dataframe (pl.DataFrame)

    """
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
                          sorted_operators, selected_date: datetime, color_filter: str) -> st.plotly_chart:
    """ Creates a plotly timeline chart with a filtered view (by day and category) of transactions
    Each row corresponds to an operator that has at least one transaction on that day.

    Args:
        df_transactions:  Transaction DataFrame
        sorted_operators: Operators (after filtering); used to create filtered view of y-axis
        selected_date: Day to show transactions on (date.datetime)
        color_filter: How to color the chart (by Operator ID or by Transaction Type)

    Returns:

    """
    fig = px.timeline(df_transactions, x_start=Trans.START_TIME,
                      x_end=Trans.END_TIME, y=Trans.OPERATOR_ID, color=color_filter)
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


    # IMPORTANT: assuming 7:00 and 19:00 are cutoffs for shift changeover
    # Hardcoded for 2020
    fig.add_vline(x=datetime(2020, selected_date.month, selected_date.day, 19), line_dash="dash", line_color="black", line_width=1)
    fig.add_vline(x=datetime(2020, selected_date.month, selected_date.day, 7), line_dash="dash", line_color="black", line_width=1)
    return st.plotly_chart(fig, theme=None)

def create_operator_freq_table(df_transactions: pl.DataFrame, date_min, date_max) -> st.dataframe:
    """ Creates a filtered view of dataframe, counting how many transactions are done by each operator in time period.
    Stats generated include: count (transactions), mean duration (of transactions), and mean gap (between transactions).
    Args:
        df_transactions: Transaction DataFrame
        date_min: Minimum date to filter by
        date_max: Maximum date to filter by

    Returns:
        st.dataframe
    """
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


