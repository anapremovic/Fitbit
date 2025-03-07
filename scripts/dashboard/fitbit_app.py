import streamlit as st

home_page = st.Page("home_page.py", title="Home", icon="📌")
exercise_page = st.Page("exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

pg.run()
