import polars as pl
from polars import col
import plotly.graph_objects as go
import plotly.express as px
from jsr.utils.col_namespace import Sched, Ship, Trans
from jsr.utils.plotting import plot_write_image


def ship_plot_total_value_over_time(df_shipments: pl.DataFrame,
                                    write_image=False) -> go.Figure:
    """ Shows total summary of shipment values for each day in the data
    Args:
        df_shipments: Shipments dataframe
        write_image: If True, write image to file

    Returns:
        Plotly figure
    """

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
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis_title="Day", xaxis_title_font_size=26,
        yaxis_title="Total", yaxis_title_font_size=26,
        title="Total Daily Value of Shipments",
        title_y=0.99,
        title_font_size=32,
        font_family="Overpass"
    )

    # Annotation - "Average" Box
    fig.add_annotation(
        xref="paper",
        x=1,
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

    if write_image:
        plot_write_image(fig, output_name="ship_plot_total_value_over_time")

    fig.update_xaxes(title_standoff=2)
    fig.update_yaxes(title_standoff=2)
    return fig

def ship_plot_max_value_over_time(df_shipments: pl.DataFrame,
                                    write_image=False) -> go.Figure:
    """ Shows summary of maximum shipment value for each day in the data
    Args:
        df_shipments: Shipments dataframe
        write_image: If True, write image to file

    Returns:
        Plotly figure
    """

    # Extract Total values and mean time (for red hline)
    total_values_by_day = (
        df_shipments
        .sort(Ship.SHIP_DATE)
        .group_by_dynamic(Ship.SHIP_DATE, every="1d")
        .agg(max_value=col(Ship.VALUE).max().alias("Max Value"))
    )

    # Initial bar chart
    fig = px.bar(total_values_by_day, x=Ship.SHIP_DATE, y="max_value",
                 template="seaborn")
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis_title="Day", xaxis_title_font_size=26,
        yaxis_title="Total", yaxis_title_font_size=26,
        title="Max Daily Value of Shipments",
        title_y=0.99,
        title_font_size=32,
        font_family="Overpass"
    )

    if write_image:
        plot_write_image(fig, output_name="ship_plot_max_value_over_time")

    fig.update_xaxes(title_standoff=2)
    fig.update_yaxes(title_standoff=2)
    return fig
