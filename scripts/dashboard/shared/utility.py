import streamlit as st

from scripts.database import FitbitDatabase

def display_filters(disabled: bool) -> None:
    fitbit_db: FitbitDatabase = st.session_state["fitbit_db"]

    st.sidebar.header("Filters")

    st.sidebar.selectbox(
        "User ID",
        key="selected-user",
        options=("All",) + fitbit_db.user_ids,
        disabled=disabled,
    )

    left, right = st.sidebar.columns(2)
    with left: 
        st.date_input(
            "Start date",
            key="selected-start-date",
            value=st.session_state.get("selected-start-date", fitbit_db.min_date),
            min_value=fitbit_db.min_date,
            max_value=st.session_state.get("selected-end-date", fitbit_db.max_date),
            disabled=disabled,
        )
    with right:
        st.date_input(
            "End date",
            key="selected-end-date", 
            value=st.session_state.get("selected-end-date", fitbit_db.max_date),
            min_value=st.session_state.get("selected-start-date", fitbit_db.min_date),
            max_value=fitbit_db.max_date,
            disabled=disabled,
        )

