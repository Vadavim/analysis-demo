import polars as pl
from polars import col
from polars import selectors as cs
import plotly.graph_objects as go
import datetime
import plotly.express as px
from jsr.utils.col_namespace import Sched, Ship, Trans
from jsr.utils.plotting import plot_write_image, default_figure_settings


def ship_demo1_transaction_schedule(df_transactions: pl.DataFrame, write_image=False) -> go.Figure:
    """ Show timeline plot of operator schedules, colored by shift ID
    Args:
        df_transactions: Transactions DataFrame
        write_image: If true, write image to disk

    Returns:
        Plotly figure
    """
    filtered_df = (
        df_transactions
        .filter(col(Trans.START_TIME).dt.day() == 14)
        .filter(col(Trans.START_TIME).dt.month() == 11)
        .sort("OPERATOR_ID")
        .with_columns(col(Trans.OPERATOR_ID).cast(str))
    )

    # Enforce operator order (based on Shift ID)
    operator_order = filtered_df.sort(Trans.FEAT_SHIFT_ID)[Trans.OPERATOR_ID].unique(maintain_order=True).to_list()

    fig = px.timeline(filtered_df, x_start="START_TIME",
                      x_end="END_TIME", y="OPERATOR_ID", color=Trans.FEAT_SHIFT_ID)
    fig.update_traces(width=0.98)
    fig.update_layout(bargap=0.01, bargroupgap=0.0)
    fig.update_yaxes(tickfont_size=4)

    default_figure_settings(fig,
                            x_label="Time", y_label="Operator ID", title="Shift Breakdown for Nov 14th")

    # Shift changeover times
    fig.add_vline(x=datetime.datetime(2020, 11, 14, 19), line_dash="dash", line_color="black", line_width=1)
    fig.add_vline(x=datetime.datetime(2020, 11, 14, 7), line_dash="dash", line_color="black", line_width=1)
    fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=operator_order,  # ← your fixed list here
        )
    )

    if write_image:
        plot_write_image(fig, output_name="transaction_by_shift_on_nov_14th")
    return fig

def ship_demo2_transaction_schedule(df_transactions: pl.DataFrame, write_image=False) -> go.Figure:
    """ Show timeline plot of operator schedules, colored by transaction type

    Args:
        df_transactions: Transactions DataFrame
        write_image: If true, write image to disk

    Returns:
        Plotly figure
    """
    filtered_df = (
        df_transactions
        .filter(col(Trans.START_TIME).dt.day() == 14)
        .filter(col(Trans.START_TIME).dt.month() == 11)
        .sort("OPERATOR_ID")
        .with_columns(col(Trans.OPERATOR_ID).cast(str))
    )

    # Enforce operator order (based on Shift ID)
    operator_order = filtered_df.sort(Trans.FEAT_SHIFT_ID)[Trans.OPERATOR_ID].unique(maintain_order=True).to_list()

    fig = px.timeline(filtered_df, x_start="START_TIME",
                      x_end="END_TIME", y="OPERATOR_ID", color=Trans.TRANSACTION_TYPE
                      )
    fig.update_traces(width=0.98)
    fig.update_layout(bargap=0.01, bargroupgap=0.0)
    fig.update_yaxes(tickfont_size=4)

    default_figure_settings(fig,
                            x_label="Time", y_label="Operator ID", title="Transaction Type Breakdown for Nov 14th")

    # Shift changeover times
    fig.add_vline(x=datetime.datetime(2020, 11, 14, 19), line_dash="dash", line_color="black", line_width=1)
    fig.add_vline(x=datetime.datetime(2020, 11, 14, 7), line_dash="dash", line_color="black", line_width=1)

    fig.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=operator_order,  # ← your fixed list here
        )
    )

    if write_image:
        plot_write_image(fig, output_name="transaction_by_type_on_nov_14th")
    return fig

def ship_demo_outlier(df_transactions: pl.DataFrame, write_image=False) -> go.Figure:
    """ Shows an example of a day with an unusually long transaction
    Args:
        df_transactions:  Transactions DataFrame
        write_image:  If true, write image to disk

    Returns:
        Plotly figure
    """
    filtered_df = (
        df_transactions
        .filter(col(Trans.START_TIME).dt.day() == 24)
        .filter(col(Trans.START_TIME).dt.month() == 10)
        .sort("OPERATOR_ID")
        .with_columns(col(Trans.OPERATOR_ID).cast(str))
    )

    fig = px.timeline(filtered_df, x_start="START_TIME",
                      x_end="END_TIME", y="OPERATOR_ID", color=Trans.TRANSACTION_TYPE)
    fig.update_traces(width=0.98)
    fig.update_layout(bargap=0.01, bargroupgap=0.0)
    fig.update_yaxes(tickfont_size=4)

    default_figure_settings(fig,
                            x_label="Time", y_label="Operator ID", title="Example of an outlier")

    # fig.add_vline(x=datetime.datetime(2020, 11, 14, 19), line_dash="dash", line_color="black", line_width=1)
    # fig.add_vline(x=datetime.datetime(2020, 11, 14, 7), line_dash="dash", line_color="black", line_width=1)

    if write_image:
        plot_write_image(fig, output_name="transaction_outlier_example")
    return fig
