from typing import Dict

import streamlit as st
from datetime import datetime
import polars as pl

from jsr.utils.processing import process_dataframes

def component_time_picker(tmin: datetime, tmax: datetime) -> datetime.date:
    """
    Args:
        tmin:  Minimum date allowed by the date picker
        tmax: Maximum data allowed by the date picker

    Returns:
        Chosen date (datetime.date)
    """
    selected_date = st.date_input(
        label       = "Select a day",
        value       = tmin,
        min_value   = tmin,
        max_value   = tmax,
        format      = "YYYY/MM/DD",
        help        = "Only dates with data are available."
    )
    return selected_date

def get_dataframes() -> Dict[str, pl.DataFrame]:
    """ Dataframes are stored in a session state to be shared between pages.
    Returns
        dict[str, pl.DataFrame]: "shipments", "transactions", "schedule"
    """
    if "dataframes" not in st.session_state:
        st.session_state.dataframes = process_dataframes("data/")
    return st.session_state.dataframes
