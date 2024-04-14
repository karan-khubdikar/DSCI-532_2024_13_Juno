from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go

from data import df
import callbacks
from components import title, global_widgets, card_women, card_men, industry, line_chart, barchart, barchart2, map
# Adding new components in a new line so it is easier to isolate anything new which might be causing problems
from components import juno_explanation, dataset_description, project_description, collapse_button, collapse_section, card_ratio
from dash import State

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(title, style={"margin-top": "5px"}, className="text-center"),
    ]),
    dbc.Col(html.Div(collapse_button), className="text-center"),
    dbc.Row([
        dbc.Col(collapse_section, style={"margin-top": "10px"})
    ]),
    # dbc.Row(dbc.Col(project_description)),
    # dbc.Row(dbc.Col(juno_explanation)),
    dbc.Row(dbc.Col(dataset_description, style={"margin-top": "10px"})),
    dbc.Row([
        dbc.Col([
                dbc.Card([dbc.Col(industry), dbc.Col(card_women), dbc.Col(card_men), dbc.Col(card_ratio)], style={
        'background-color': '#F5F5F5',
        'padding': 15,
        'border-radius': 3,
        'width':'80%',
        'margin-bottom': '20px'
    }, ),
                dbc.Row(dbc.Col(global_widgets, width=6)),
            ],
            sm= "5",
        ), 
        dbc.Col([dvc.Vega(id="map",opt = {"rendered":"svg", "actions":False})], width = 1), 
    ]), 
    # bear with the squishing for now
#     dbc.Row([
#     dbc.Col(industry, width=3),
#     dbc.Col(card_women, width=3),
#     dbc.Col(card_men, width=3),
#     dbc.Col(card_ratio, width=3)
# ], style={
#     'background-color': '#F5F5F5',
#     'padding': 15,
#     'border-radius': 3
# }),
    dbc.Row([dbc.Col(dvc.Vega(id='line-chart'))]),
    dbc.Row([dbc.Col(dcc.Graph(id='bar-chart')), dbc.Col(dcc.Graph(id='bar2-chart'))]),
    html.Footer([
        html.P(''),
        html.Hr(),
        # Transferred information to the top
        # html.P(
        #     'This project scrutinizes the gender disparity in top-level leadership roles within Canadian corporations '
        #     'across multiple sectors. Leveraging gender-disaggregated data, we aim to reveal the potential influence '
        #     'of gender balance in decision-making roles on more effective and inclusive policies. The displayed dashboards '
        #     'are filtered based on the selected tags, showing only those that match all selected tags. Tag counts are updated '
        #     'dynamically to reflect the number of visible dashboards after filtering. For optimal viewing, this dashboard '
        #     'is recommended for a full-width window.',
        #     style={'font-size': '12px', 'margin-bottom': '10px'}),        
        html.P('Last updated on April 13, 2024.', style={'font-size': '12px', 'margin-bottom': '10px'}),
        html.A('The source code can be found on GitHub.', href='https://github.com/UBC-MDS/DSCI-532_2024_13_Juno', style={'font-size': '14px', 'margin-bottom': '10px'})
    ]),

])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port = 8052)