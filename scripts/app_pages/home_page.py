import streamlit as st
 
from scripts.diagrams.home_diagrams import HomeDiagrams

st.session_state["current-page"] = "home"

@st.cache_resource
def get_home_diagrams():
    return HomeDiagrams(st.session_state["fitbit-db"])
home_diagrams = get_home_diagrams()

left, div, right = st.columns([2, 0.02, 3])
with left:
    st.subheader("Survey Details")
    days, participants = st.columns(2)
    with days:
        st.plotly_chart(home_diagrams.get_number_of_days())
    with participants:
        st.plotly_chart(home_diagrams.get_number_of_participants())
with div:
    st.html(
        '''
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 2px solid rgba(49, 51, 63, 1);
                    height: 170px;
                    margin: auto;
                }
            </style>
        '''
    )
with right:
    st.subheader("Collective Metrics")
    steps, distance, active_min = st.columns(3)
    collective_metrics = home_diagrams.get_collective_metrics()
    with steps:
        st.plotly_chart(collective_metrics[0])
    with distance:
        st.plotly_chart(collective_metrics[1])
    with active_min:
        st.plotly_chart(collective_metrics[2])

steps, active_time = st.columns([0.9, 1.1])
bar_plots = home_diagrams.get_steps_and_active_bar_plot()
with steps:
    st.plotly_chart(bar_plots[0])
with active_time:
    st.plotly_chart(bar_plots[1])
