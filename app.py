import pandas as pd
import streamlit as st
import plotly.express as px

import helper
import preprocessor

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)


st.sidebar.title("Info-Olympics")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Overall Analysis', 'Athlete-wise Analysis',  'Country-wise Analysis', 'Medal Tally')
)

# code to show medal tally and its sub categories

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Medal Tally")
    if selected_year != 'overall' and selected_country == 'overall':
        st.title("Medal Tally in " + str(selected_year) + ' Olympics')
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + "'s Overall performance")
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + "'s performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

# code to show overall analysis

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Overall Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.subheader(editions)
    with col2:
        st.header("Cities")
        st.subheader(cities)
    with col3:
        st.header("Sports")
        st.subheader(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.subheader(events)
    with col2:
        st.header("Athletes")
        st.subheader(athletes)
    with col3:
        st.header("Nations")
        st.subheader(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Year", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("Most successful athletes")
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'overall')

    selected_sport = st.selectbox('Select a Sport', sports_list)
    x = helper.most_succesful(df, selected_sport)
    st.table(x)

# code  for country wise analysis

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selectedCountry = st.sidebar.selectbox('Select a country', country_list)

    country_df = helper.year_wise_medal_tally(df,selectedCountry)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selectedCountry + "'s Medal tally over the years")
    st.plotly_chart(fig)

    st.title("top Athletes of " + selectedCountry)
    top15_df = helper.most_succesful_countrywise(df,selectedCountry)
    st.table(top15_df)

# code for athlete wise analysis

if user_menu == 'Athlete-wise Analysis':
    st.sidebar.title('Athlete-wise Analysis')

    sport = helper.sport_list_func(df)

    selected_sports = st.sidebar.selectbox('Select Sports',sport)

    athlete = helper.athlete_list_func(df, selected_sports)

    if selected_sports == 'overall':
        st.title("All players who won medals")
        selected_athlete = 'null'
    else:
        selected_athlete = st.sidebar.selectbox('Select Athlete', athlete)


    if selected_sports != 'overall' and selected_athlete == 'overall':
        st.title("Player who won medals in " + selected_sports)
    if selected_sports != 'overall' and selected_athlete != 'overall':
        st.title(selected_athlete + "'s medals in " + selected_sports)

    data = helper.athlete_wise_analysis_func(df,  selected_sports, selected_athlete)
    st.table(data)


