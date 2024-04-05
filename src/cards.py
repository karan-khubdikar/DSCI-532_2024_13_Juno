from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
from vega_datasets import data
import pandas as pd
import os

# current_directory = os.getcwd()
# print(f'Current directory: {current_directory}')
card_data = pd.read_csv('data/filtered/cards_data.csv')

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
title = [html.H1('Juno'), html.Br()]
province_columns = card_data['GEO'].unique()
industry_columns = card_data['Industry'].unique()
time_columns = card_data['REF_DATE'].unique()

global_widgets = [
    dbc.Label('Filter on Province'),
    dcc.Dropdown(id='province-filter', options=province_columns, value='Canada, total'),
    html.Br(),
    dbc.Label('Filter on Industry'),
    dcc.Dropdown(id='industry-filter', options=industry_columns, value='Total all industries'),
    dbc.Label('Filter on Year'),
    dcc.Dropdown(id='year-filter', options=time_columns, value= 2016)  # Might want to consider a multi-filter option for year
]
card_women = dbc.Card(id='card-women')
card_men = dbc.Card(id='card-men')


# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(
            [
                dbc.Row([dbc.Col(card_women), dbc.Col(card_men)])
            ],
            md=8
        )
    ])
])

# Server side callbacks/reactivity
@callback(
    Output('card-women', 'children'),
    Output('card-men', 'children'),
    Input('province-filter', 'value'),
    Input('industry-filter', 'value'),
    Input('year-filter', 'value'),
)
def calculate_proportion(province_filter, industry_filter, year_filter):
    # There is no need to drop na for card_data because there are no NAs in this filtered dataset, but this is the code to check
    # For this and drop NA if needed in the future
    # print(f'Card_df shape: {card_data.shape}')
    # print(f"NA values in card df: {card_data['VALUE'].isna().sum()}")
    # card_data.dropna(subset=['VALUE'], inplace=True)

    # Implementing filtering based on widgets
    # Bug with filtering everything at once - will filter step wise until I find a solution
    geo_filtered_data = card_data[card_data['GEO'] == province_filter]
    industry_filtered_data = geo_filtered_data[geo_filtered_data['Industry'] == industry_filter]
    filtered_data = industry_filtered_data[industry_filtered_data['REF_DATE'] == year_filter]  # Final filter

    women_card_df = filtered_data.query('Gender == "Women"')
    men_card_df = filtered_data.query('Gender == "Men"')
    # print(f"NA values in women df: {women_card_df.isna()}")
    # print(f"NA values in men df: {men_card_df.isna()}")
    total_people = filtered_data['VALUE'].sum()
    total_women = women_card_df['VALUE'].sum()
    total_men = men_card_df['VALUE'].sum()
    prop_women = (total_women / total_people) * 100
    prop_men = (total_men / total_people) * 100

    card_women_content = [
        dbc.CardHeader('Overall Proportion of Women in this Subset (%)'),
        dbc.CardBody(f'{round(prop_women, 2)} %')
    ]
    card_men_content = [
        dbc.CardHeader('Overall Proportion of Men in this Subset (%)'),
        dbc.CardBody(f'{round(prop_men, 2)} %')
    ]
    return card_women_content, card_men_content

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8051)  # Can remove/change port later