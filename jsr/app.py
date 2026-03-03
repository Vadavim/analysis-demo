import streamlit as st
from jsr.utils.processing import process_dataframes

if "dataframes" not in st.session_state:
    st.session_state.dataframes = process_dataframes("data/")

pages = {
    "Description": [
        st.Page("pages/description.py", title="Overview", icon=":material/description:")
    ],
    "Shipments": [
        st.Page("pages/page_shipment.py", title="Shipment Explorer", icon=":material/analytics:"),
    ],

    "Transactions & Operators": [
        st.Page("pages/page_operator_timeline.py", title="Operator Timelines", icon=":material/timeline:"),
        st.Page("pages/page_transaction_overview.py", title="Transaction Overview", icon=":material/forklift:")
    ],

    "[Incomplete]": [
        st.Page("pages/page_operator.py", title="Operator Stats", icon=":material/group:")
    ]

}

pg = st.navigation(pages, position="sidebar")
pg.run()



