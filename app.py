import streamlit as st
import numpy as np

from src.inputs import get_standings, get_fixtures, get_standings, filter_fixtures
from src.simulate import simulate_scenarios
from src.streamlit import create_footer, hide_row_headers, hide_full_screen, reduce_whitespace

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write('<style>div.row-widget.stSpinner > div{text-align:center;}</style>', unsafe_allow_html=True)

st.markdown(hide_row_headers(), unsafe_allow_html=True)
st.markdown(hide_full_screen(), unsafe_allow_html=True)
st.markdown(reduce_whitespace(), unsafe_allow_html=True)

st.header("IPL Qualifier Predictor")
st.markdown("#### Current Standings and Qualification Chances")
progress = st.progress(0)
spinner = st.empty()
st.sidebar.markdown("### Choose number of timelines to visit!")
iterations = int(st.sidebar.slider("# simulations", 500, 10000, 1465)/2)

fixtures = get_fixtures()
standings = get_standings()
filtered_fixtures = filter_fixtures(fixtures, standings)
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

with st.expander("Methodology ⓘ"):
    st.markdown("""
         The Model is a simple monte carlo simulation where either team has an equal (50%) chance of winning each match and simulating as many timelines to find the probabilities.
         A team is considered:
         - Top 2 if it is in the top 2 and the 3th team has lesser points, or Top 4 if it is in the top 4 and 5th team has lesser points
         - Not in Top 4 if the team has less points is in the bottom 4 and has lesser points than the 4th team,
         - Top 2/Top 4 on NRR if a team has the same points as the 3rd/5th team appropariately.

         The source code can be found at the [source github repo](https://github.com/alexsanjoseph/ipl-scenario-builder)
     """)

footer_text = "Made with ❤ by <a style='display: block;' href=\"https://blog.alexsanjoseph.com//\" target=\"_blank\">Alex Joseph</a> with Streamlit, Marvel and ESPNCricinfo <a style='display: block; text-align: center;' href=\"https: // blog.alexsanjoseph.com//\" target=\"_blank\"></a> (click the > on top left on mobile to access the scenario sidebar)"
st.markdown(create_footer(footer_text), unsafe_allow_html=True)
