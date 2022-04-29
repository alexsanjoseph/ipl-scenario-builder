# IPL Scenario Builder

This is a simple app to predict the qualification chances of different IPL teams by using the match fixtures and current standings and making Monte Carlo simulations to find the probability of each team winning.

Flow:

- Get the fixtures from https://www.icccricketschedule.com
- Get the current standings from http://www.espncricinfo.com
- Find out the games starting after current time (fixture times + 4 hours)
- Do many simulations on which team wins each match.
- Calculate the summary statistics as probabilities

A team is considered:

- qualified (Yes %) if it is in the top 4 and the 5th team has lesser points,
- not qualified (No %) if the team has less points is in the bottom 4 and has lesser points than the 4th team,
- qualified on NRR (on NRR%) if a team has the same points as the 5th team.

Expected Number of points is the average number of points across all simulations.

The app is hosted using Streamlit Cloud [here](https://share.streamlit.io/alexsanjoseph/ipl-scenario-builder/main/app.py)
