import numpy as np


def fetch_medal_tally(df, year, country):
    global temp_df
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.insert(0, 'overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'count' : col},inplace=True)
    return nations_over_time

def most_succesful(df, selected_sport):
    tempdf=df.dropna(subset=['Medal'])

    if selected_sport != 'overall':
        tempdf = tempdf[tempdf['Sport']==selected_sport]

    x = tempdf['Name'].value_counts().reset_index().head(10).merge(df, how="left")[
        ['Name', 'Sport', 'region','count']].drop_duplicates('Name')
    x.rename(columns={'count' : 'Medals'},inplace=True)

    return x


def year_wise_medal_tally(df,country):
    country_wise_df = df.dropna(subset=['Medal'])
    country_wise_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                    inplace=True)
    new_df = country_wise_df[country_wise_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def most_succesful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,how="left")[['Name','Sport','count']].drop_duplicates('Name')
    x.rename(columns={'count' : 'Medals'},inplace=True)
    return x

def sport_list_func(df):
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')
    return  sport_list

def athlete_list_func(df,sport):
    if sport == 'overall':
        athlete_list = df['Name'].unique().tolist()
        athlete_list.sort()
        athlete_list.insert(0, 'overall')
    else:
        athlete_list = df[df['Sport']==sport]['Name'].unique().tolist()
        athlete_list.sort()
        athlete_list.insert(0, 'overall')

    return athlete_list


def athlete_wise_analysis_func(df,selected_sport,selected_athlete):
    athlete_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if selected_sport == 'overall' and selected_athlete == 'null':
        x = athlete_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Name').reset_index()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x = x.loc[x['Total'] != 0]

        return x
    if selected_sport != 'overall' and selected_athlete == 'overall':
        new = athlete_df[athlete_df['Sport'] == selected_sport]
        x = new.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Name').reset_index()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x = x.loc[x['Total'] != 0]

        return x
    if selected_sport != 'overall' and selected_athlete != 'overall':
        new = athlete_df[athlete_df['Sport'] == selected_sport]
        final_data = new[new["Name"] == selected_athlete]
        x = final_data[['Gold', 'Silver', 'Bronze']].sum().reset_index()

        return x