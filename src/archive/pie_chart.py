from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
#from vega_datasets import data
import pandas as pd

df = pd.read_csv('data/filtered/pie_chart_data.csv')


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='pie-chart', spec={}),
    html.P(html.Br()),
    html.Label('Select a Year'),
    dcc.Dropdown(id='year', options=df["REF_DATE"].unique().tolist(), value = 2016),
    html.Label('Select an Industry'),
    dcc.Dropdown(id='industry', options = df["Industry"].unique().tolist(), value ='Finance')
])

# Server side callbacks/reactivity
@callback(
    Output('pie-chart', 'spec'),
    Input('year', 'value'),
    Input('industry', 'value'),
)

def create_chart(year, industry):

    # Issue is with industry and year datatype - not recognised by pandas, so it returns empty df (filtered_df)
    filtered_df = df[(df["Industry"] == industry) & (df["REF_DATE"] == year)]

    
    chart = alt.Chart(filtered_df).mark_arc().encode(
        theta="VALUE",
        color="Gender"
    )

    return chart.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)