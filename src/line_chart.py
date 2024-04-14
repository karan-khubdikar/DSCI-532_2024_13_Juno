from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

df = pd.read_csv('data/filtered/province_data.csv')
card_data = pd.read_csv('data/filtered/cards_data.csv')
time_columns = card_data['REF_DATE'].unique()
province_columns = card_data['GEO'].unique()

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='line-chart', spec={}),
    html.P(html.Br()),
    dbc.Label('Filter on Province'),
    dcc.Dropdown(id='province-filter', options=province_columns, value='Canada, total'),
    html.Br(),
    dbc.Label('Filter on Year'),
    dcc.Dropdown(id='year-filter', options=time_columns, value= 2016)
])

# Server side callbacks/reactivity
@callback(
    Output('line-chart', 'spec'),
    [Input('province-filter', 'value'),
     Input('year-filter', 'value')]
)
def create_chart(prov, selected_year):
    filtered_df = df[(df["GEO"] == prov)]

    canada_total = {
    'Year': [2016, 2017, 2018, 2019, 2020],
    'Ratio': [0.422879, 0.424134, 0.432834, 0.433269, 0.457492]
    }
    canada_total_ratio = pd.DataFrame(canada_total)

    prov_ratio_values = filtered_df.apply(lambda row: row['VALUE'] / filtered_df.loc[(filtered_df['REF_DATE'] == row['REF_DATE']) & (filtered_df['Gender'] == 'Men'), 'VALUE'].iloc[0], axis=1)
    prov_ratio = prov_ratio_values[prov_ratio_values != 1]

    province_gender_ratio = pd.DataFrame({
    'Year': range(2016, 2021),
    'Ratio': prov_ratio
    })

    chart = alt.Chart(province_gender_ratio).mark_line().encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year')),
        y=alt.Y('Ratio:Q', axis=alt.Axis(title='Ratio (Women/Men)')),
        tooltip=['GEO:N', 'Ratio:Q'],
    ).properties(
        title='Ratio of Women v/s Men in Executive Positions in {} Over the Years'.format(prov),
        width=1200,
        height=200
    )

    if selected_year is not None:
        rule = alt.Chart(pd.DataFrame({'selected_year': [selected_year]})).mark_rule(color='red').encode(
            x='selected_year:O'
        ).transform_filter(
            alt.FieldEqualPredicate(field='selected_year', equal=selected_year)
        )
        chart_with_marker = chart + rule
    else:
        chart_with_marker = chart
    
    canada_tot_ratio = alt.Chart(canada_total_ratio).mark_line(strokeDash=[1,1]).encode(
        x='Year:O',
        y='Ratio:Q'
    )

    chart_with_marker = (chart_with_marker + canada_tot_ratio).configure_legend(
        orient='right'
    )

    return chart_with_marker.configure_axis(
        labelAngle=0
    ).to_dict()


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)