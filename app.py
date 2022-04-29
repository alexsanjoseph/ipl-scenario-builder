import streamlit as st
import numpy as np

from src.inputs import get_standings, get_fixtures, get_standings
from src.simulate import simulate_scenarios, filter_fixtures
from src.summarize import summarize_results
from src.outputs import write_output

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write('<style>div.row-widget.stSpinner > div{text-align:center;}</style>', unsafe_allow_html=True)

footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Made with ❤ by <a style='display: block; text-align: center;' href="https://blog.alexsanjoseph.com//" target="_blank">Alex Joseph</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.header("IPL Qualifier Predictor")
st.markdown("#### Current Standings and Qualification Chances")
progress = st.progress(0)
spinner = st.empty()
st.sidebar.markdown("### Choose number of timelines to check!")
iterations = int(st.sidebar.slider("Iterations", 500, 10000, 1465)/20)

fixtures = get_fixtures()
standings = get_standings()
filtered_fixtures = filter_fixtures(fixtures)
if 'winners' not in st.session_state:
    st.session_state['winners'] = ["Random"] * filtered_fixtures.shape[0]


def recalculate():
    filtered_fixtures_fixed = filtered_fixtures
    for i, x in enumerate(st.session_state['winners']):
        if x != "Random":
            filtered_fixtures_fixed.iloc[i, :] = x
    return filtered_fixtures_fixed


table_slot = st.empty()


st.sidebar.markdown("### Qualification Scenarios")
st.sidebar.markdown(
    "*Choose a winning team for each match or leave it at random for a 50% chance of either team winning...*")
for i in range(filtered_fixtures.shape[0]):
    # for i in range(5):
    box_array = ["Random", filtered_fixtures.iloc[i, 0], filtered_fixtures.iloc[i, 1]]

    st.session_state['winners'][i] = st.sidebar.radio(
        f"Match {filtered_fixtures.index[i]}: {filtered_fixtures.iloc[i, 2].strftime('%a, %d %b %Y %H:%M')}",
        box_array,
        box_array.index(st.session_state['winners'][i])
    )

filtered_fixtures_fixed = recalculate()
# with st.spinner('Calculating scenarios...'):
spinner.markdown("![Alt Text](https://c.tenor.com/nDhUSRc7Q-8AAAAd/timeline-doctor-strange.gif)")
all_results = simulate_scenarios(filtered_fixtures_fixed, standings, iterations, progress)
spinner.empty()

table_slot.table(all_results)
