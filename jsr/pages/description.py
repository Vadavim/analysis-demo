import streamlit as st

st.title("Overview")
st.markdown(
    """
    This dashlit app is meant to highlight some potential interfaces that could be developed to help stakeholders.
    """
)
st.divider()

st.header("Shipment Explorer")

st.markdown("""
This is meant to allow stakeholders to browse through important shipment metrics (count, total value, etc). 
It can also show breakdowns by order line, and provides a filter for order line IDs of interest.
""")

st.header("Operator Timelines")

st.markdown("""
This is meant to highlight breakdowns of operator transaction on a daily, weekly, or monthly basis. 
It utilizes a timeline chart.
""")

st.header("Transaction Overview")

st.markdown("""
This interface provides an overview of transaction broken down by **shift** over a week, month, or year.
It also allows for filtering by transaction type and can also display the number of operators on that shift.
""")
