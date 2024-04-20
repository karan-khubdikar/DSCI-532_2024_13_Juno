from dash import Dash, dcc, callback, Output, Input, html, State
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go

from data import df
import callbacks
from components import title, global_widget_1, global_widget_2, card_women, card_men, industry, line_chart, barchart, barchart2, map
from components import dataset_description, collapse_button, collapse_section, card_ratio  # Breaking up the line

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], title = "Juno")
server = app.server

# Layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(title, style={"margin-top": "5px",
                              'backgroundColor': '#800080', 
                              'padding': 20, 'color': 'white'}, 
                              className="text-center"),
    ]),
    dbc.Col(html.Div(collapse_button), className="text-center"),
    dbc.Row([
        dbc.Col(collapse_section, style={"margin-top": "10px"})
    ]),
    # dbc.Row(dbc.Col(dataset_description, style={"margin-top": "10px"})),
    dbc.Row([
                dbc.Card([
                    dbc.CardHeader(html.H3("National averages by industry"), style={'background-color': 'white',
                                'padding': 5,
                                'border-radius': 1,
                                'width':'100%',
                                'margin-bottom': '20px'}),
                    dbc.Col(industry, md = 'auto'),
                          dbc.Row([ 
                            dbc.Col(card_women), 
                            dbc.Col(card_men), 
                            dbc.Col(card_ratio)]),], 
                         style={'background-color': '#F5F5F5',
                                'padding': 5,
                                'border-radius': 1,
                                'width':'100%',
                                'margin-bottom': '20px'})]),
    dbc.Row(dvc.Vega(id="map",opt = {"rendered":"svg", "actions":False},
                style={'background-color': '#F5F5F5',
                       'padding': 15,
                       'width':'100%'})),
    dbc.Row([
        dbc.Card([
            dbc.Row([
            dbc.Col(global_widget_1),
            dbc.Col(global_widget_2)])
            ]),
            ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(dvc.Vega(id='line-chart'), md =5),
                # style={"margin-top": "10px", 
                #        "margin-bottom": "10px", 
                #        "margin-left": "20px"}, md = 5),
    ]),
    html.P(''),
    html.P(''),
    dbc.Card([
       dbc.Row([dbc.Col(dcc.Graph(id='bar-chart'),style={"margin-top": "10px", "margin-bottom": "10px"}, md =5), 
             dbc.Col(dcc.Graph(id='bar2-chart'),style={"margin-top": "10px", "margin-bottom": "10px"}, md = 7)]),
             ], style={'background-color': '#F5F5F5',
                                'padding': 0,
                                'border-radius': 1,
                                'width':'100%',
                                'margin-bottom': '10px'}),
    html.Footer([
        html.P(''),
        html.Hr(),       
        html.P('Last updated on April 19, 2024.', style={'font-size': '12px', 'margin-bottom': '10px'}),
        html.A('The source code can be found on GitHub.', href='https://github.com/UBC-MDS/DSCI-532_2024_13_Juno', style={'font-size': '14px', 'margin-bottom': '10px'})
    ]),
])


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port = 8052)