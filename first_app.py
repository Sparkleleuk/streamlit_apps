from matplotlib import interactive
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

DATA_SOURCE = "marketACSRanking.csv"
@st.cache
def load_data():
    data = pd.read_csv(DATA_SOURCE)
    return data

data = load_data()

# sidebar 
cities_filter = list(set(data['Metropolitan Statistical Area']))
city_option = st.sidebar.selectbox(
    'Select a City',
    options=(cities_filter))
      
decade_option = st.sidebar.select_slider(
    'Select a Decade',
    options=[2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
    )

scenario_option = st.sidebar.radio(
    'Select an Emissions Scenario',
    ('RCP 2.6', 'RCP 4.5', 'RCP 6.0', 'RCP 8.5'))

st.sidebar.write('You selected:', city_option, decade_option, scenario_option)

add_button = st.sidebar.button("Download Report")

# Main section

st.title("TCS Adaptive Contribution Score")
st.write("The ACS captures the potential to positively contribute to the climate adaptivity of the market. It is based on the hazard exposure, social vulnerability, and economic strength of the market. The value of each component represents its percentile rank relative to other US markets. The overall score is based on an aggregation of relative ranks of the components.")

st.header(city_option)

st.subheader("ACS: 0.508/1")

st.write("Brief explanation of Boston's overall ACS.")

map_data = pd.DataFrame({
    'US cities' : ['Boston', 'Kansas City', 'St. Louis', 'Denver'],
    'lat' : [42.3601, 39.0997, 38.6270, 39.7392],
    'lon' : [-71.0589, -94.5786, -90.1994, -104.9903]
})

st.map(map_data)
st.caption('_Map displays the cities covered by the TCS ACS or a heatmap?_')


# Main Section

st.subheader("Demographics")

demographic_data = {'Demographic Metric' : ['Population Census 2020', 'Population Change 2010-2020', 'Median Household Income 2015-2019', 'Per Capita Income in Past 12 Months 2015-2019', 'Persons in Poverty'],
    'Data' : ['675,647', '12.1%', '$71,115', '$44,690', '18.9%']}
st.write(pd.DataFrame.from_dict(demographic_data))
# demographic_data.style.set_properties(**{'text-align': 'left'})

st.caption('_Source: US Census Bureau_')

# Adding 2nd main section

st.header("Attribution Analysis")

boston_ranking = pd.DataFrame({
    'ACS Metrics': ["Social Vulnerability", "Climate Hazard", "Economic Strength"],
    'Scores': [0.308, 0.308, 0.077]})

boston = alt.Chart(boston_ranking).mark_bar().encode(
    x='ACS Metrics',
    y='Scores'
).interactive()
st.altair_chart(boston, use_container_width=True)

df = pd.read_csv('marketACSRanking.csv')

st.header("Comparative Analysis")

st.subheader("Percentile Ranking")
st.text("Brief explanation the city's overall ranking relative to other cities.")

overall = alt.Chart(df).mark_bar().encode(
    x='Percentile Rank:Q',
    y=alt.Y('Metropolitan Statistical Area:O', sort='-x'),
    color=alt.condition(
        alt.datum.y == 'Boston-Cambridge-Newton,MA-NH',
        alt.value('orange'),
        alt.value('steelblue')
    )
).properties(height=900)

st.altair_chart(overall, use_container_width=True)

st.subheader('By Social Vulnerability Score')

social = alt.Chart(df).mark_bar().encode(
    x='SOCIAL:Q',
    y=alt.Y('Metropolitan Statistical Area:O', sort='-x'),
    color=alt.condition(
        alt.datum.y == 'Boston-Cambridge-Newton,MA-NH',
        alt.value('orange'),
        alt.value('steelblue')
    )
).properties(height=900)

st.altair_chart(social, use_container_width=True)

st.subheader('By Climate Hazard')

hazard = alt.Chart(df).mark_bar().encode(
    x='HAZARD:Q',
    y='Metropolitan Statistical Area:O',
    color=alt.condition(
        alt.datum.y == 'Boston-Cambridge-Newton,MA-NH',
        alt.value('orange'),
        alt.value('steelblue')
    )
).properties(height=900)

st.altair_chart(hazard, use_container_width=True)

st.subheader('By Economic Strength')

economy = alt.Chart(df).mark_bar().encode(
    x='ECON:Q',
    y=alt.Y('Metropolitan Statistical Area:O', sort='x'),
    color=alt.condition(
        alt.datum.y == 'Boston-Cambridge-Newton,MA-NH',
        alt.value('orange'),
        alt.value('steelblue')
    )
).properties(height=900)

st.altair_chart(economy, use_container_width=True)



