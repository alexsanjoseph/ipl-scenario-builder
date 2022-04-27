import streamlit as st
import datetime
import numpy as np

from src.inputs import get_standings, get_fixtures, get_standings
from src.simulate import simulate_scenarios, filter_fixtures
from src.summarize import summarize_results
from src.outputs import write_output

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


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

for i in range(filtered_fixtures.shape[0]):
    # for i in range(5):
    box_array = ["Random", filtered_fixtures.iloc[i, 0], filtered_fixtures.iloc[i, 1]]

    st.session_state['winners'][i] = st.radio(
        f"Match {filtered_fixtures.index[i]}",
        box_array,
        box_array.index(st.session_state['winners'][i])
    )

filtered_fixtures_fixed = recalculate()
all_results = simulate_scenarios(filtered_fixtures_fixed, standings)
table_slot.table(all_results)
