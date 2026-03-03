import streamlit as st
from datetime import datetime
from jsr.utils.processing import process_dataframes

def component_time_picker(tmin: datetime, tmax: datetime):
    selected_date = st.date_input(
        label       = "Select a day",
        value       = tmin,
        min_value   = tmin,
        max_value   = tmax,
        format      = "YYYY/MM/DD",
        help        = "Only dates with data are available."
    )
    return selected_date

def get_dataframes():
    """ Dataframes are stored in a session state to be shared between pages.
    Returns
        dict[str, pl.DataFrame]: "shipments", "transactions", "schedule"
    """
    if "dataframes" not in st.session_state:
        st.session_state.dataframes = process_dataframes("data/")
    return st.session_state.dataframes
