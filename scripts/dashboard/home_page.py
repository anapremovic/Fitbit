import streamlit as st
 
from scripts.dashboard.diagrams.home_diagrams import HomeDiagrams

@st.cache_resource
def get_home_diagrams():
    return HomeDiagrams(st.session_state["fitbit_db"])
home_diagrams = HomeDiagrams(st.session_state["fitbit_db"]) # Change this later

col1, col2, col3, col4, col5 = st.columns(5)
left, div, right = st.columns([2, 0.02, 3])
with left:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(home_diagrams.get_number_of_days())
    with col2:
        st.plotly_chart(home_diagrams.get_number_of_participants())
with div:
    st.html(
        '''
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 1);
                    height: 150px;
                    margin: auto;
                }
            </style>
        '''
    )
with right:
    col3, col4, col5 = st.columns(3)
    collective_metrics = home_diagrams.get_collective_metrics()
    with col3:
        st.plotly_chart(collective_metrics[0])
    with col4:
        st.plotly_chart(collective_metrics[1])
    with col5:
        st.plotly_chart(collective_metrics[2])
