import streamlit as st
 
from scripts.diagrams.home_diagrams import HomeDiagrams 

@st.cache_resource(show_spinner=False)
def get_home_diagrams():
    return HomeDiagrams(st.session_state["fitbit-db"])
home_diagrams = get_home_diagrams()

st.header("Fitbit Survey Results")
st.markdown("##### 📍 Chicago, IL")

left, div, right = st.columns([2, 0.02, 3])
with left:
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
                    height: 100px;
                    margin: auto;
                }
            </style>
        '''
    )
with right:
    active_min, steps, distance = st.columns(3)
    collective_metrics = home_diagrams.get_collective_metrics()
    with active_min:
        st.plotly_chart(collective_metrics[0])
    with steps:
        st.plotly_chart(collective_metrics[1])
    with distance:
        st.plotly_chart(collective_metrics[2])

steps, distance, active_time = st.columns([0.9, 0.9, 1.1])
bar_plots = home_diagrams.get_steps_distance_active_barplots()
with steps:
    st.plotly_chart(bar_plots[0])
with distance:
    st.plotly_chart(bar_plots[1])
with active_time:
    st.plotly_chart(bar_plots[2])
