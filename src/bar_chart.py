from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
#from vega_datasets import data
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('data/filtered/bar_chart_data.csv')


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.Label('Select a Year'),
    dcc.Dropdown(id='year-dropdown', options=[{'label': year, 'value': year} for year in df["REF_DATE"].unique()], value='2016'),
    html.Label('Select a Province'),
    dcc.Dropdown(id='province-dropdown', options=[{'label': province, 'value': province} for province in df["GEO"].unique()], value='Newfoundland and Labrador'),
    dcc.Graph(id='bar-chart')
])

# Server side callbacks/reactivity
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('province-dropdown', 'value')]
)
def update_chart(year, province):
    # Filter the DataFrame based on selected year and province
    filtered_df = df[(df["REF_DATE"] == year) & (df["GEO"] == province)]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Type of corporation', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside'))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside'))

    layout = go.Layout(barmode='group', title='Distribution by Type of corporation and Gender', xaxis=dict(title='Type of corporation'), yaxis=dict(title='Count'))

    return {'data': data, 'layout': layout}


# Run the app/dashboard
if __name__ == '__main__':
    app.run(port=8051, debug=True)