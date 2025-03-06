import os
import streamlit as st

pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

print(pages_dir)

# Define the pages
home_page = st.Page(f"{pages_dir}/home.py", title="Home", icon="📌")
exercise_page = st.Page(f"{pages_dir}/exercise.py", title="Exercise", icon="🏋️")
health_page = st.Page(f"{pages_dir}/health.py", title="Health", icon="❤️")

# Set up navigation
pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

# Run the selected page
pg.run()

