from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

df = pd.read_csv('data/filtered/pie_chart_data.csv')

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='line-chart', spec={}),
    html.P(html.Br()),
    html.Label('Select an Industry'),
    dcc.Dropdown(id='industry', options = df["Industry"].unique().tolist(), value ='Finance')
])

# Server side callbacks/reactivity
@callback(
    Output('line-chart', 'spec'),
    Input('industry', 'value'),
)

def create_chart(industry):

    filtered_df = df[(df["Industry"] == industry)]

    chart = alt.Chart(filtered_df).mark_line().encode(
        x = alt.X('REF_DATE:O', axis=alt.Axis(title='Year')),
        y = alt.Y('VALUE:Q', axis=alt.Axis(title='Number of People')),
        color = 'Gender:N',
        tooltip = ['Gender:N', 'VALUE:Q']
    ).properties(
        title='Number of Men and Women in {} Over the Years'.format(industry),
        width=600,
        height=400
    )

    return chart.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)