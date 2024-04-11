from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go

# Filter the data for a pie chart by province and year
df = pd.read_csv("data/raw/filtered_canada.csv")

new_df = df[(df['Type of corporation'] == 'Total all corporations') & 
            (df['Industry'] == 'Total all industries') & 
            (df["Size of enterprise"] == "Total all sizes") &
            (df["Unit of measure"] == "Number") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Unclassified province or territory")
].copy()
new_df = new_df.loc[:, ["REF_DATE", "Gender", "GEO", "VALUE"]]
new_df.head()

new_df.to_csv('data/filtered/province_data.csv', index=False)
new_df["GEO"].unique()
df = pd.read_csv('data/filtered/province_data.csv')
#############





# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


card_data = pd.read_csv('data/filtered/cards_data.csv')
# Components

title = [html.H1('Juno: Gender Equality in Executive Positions Across Canada'), html.Br()]
province_columns = card_data['GEO'].unique()#.remove('Unclassified province or territory')
province_columns = province_columns[province_columns!='Unclassified province or territory']
industry_columns = card_data['Industry'].unique()
time_columns = card_data['REF_DATE'].unique()
global_widgets = [
    dbc.Label('Filter on Province'),
    dcc.Dropdown(id='province-filter', options=province_columns, value='Canada, total'),
    html.Br(),
    dbc.Label('Filter on Year'),
    dcc.Dropdown(id='year-filter', options=time_columns, value= 2016)  # Might want to consider a multi-filter option for year
]
card_women = dbc.Card(id='card-women')
card_men = dbc.Card(id='card-men')



industry = dcc.Dropdown(id='industry-filter', options=industry_columns, value='Total all industries'),

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=6),
        dbc.Col(
            [
                dbc.Card([dbc.Col(industry), dbc.Col(card_women), dbc.Col(card_men)])

            ],
            sm= "6"
        ),
        dbc.Row(dvc.Vega(id='line-chart')),
        dbc.Row([dbc.Col(dcc.Graph(id='bar-chart')), dbc.Col(dcc.Graph(id='bar2-chart'))])
    ]),
    html.Footer([
        html.P(''),
        html.Hr(),
        html.P(
            'This project scrutinizes the gender disparity in top-level leadership roles within Canadian corporations '
            'across multiple sectors. Leveraging gender-disaggregated data, we aim to reveal the potential influence '
            'of gender balance in decision-making roles on more effective and inclusive policies. The displayed dashboards '
            'are filtered based on the selected tags, showing only those that match all selected tags. Tag counts are updated '
            'dynamically to reflect the number of visible dashboards after filtering. For optimal viewing, this dashboard '
            'is recommended for a full-width window.',
            style={'font-size': '12px', 'margin-bottom': '10px'}),        
        html.P('Last updated on April 6, 2024.', style={'font-size': '12px', 'margin-bottom': '10px'}),
        html.A('The source code can be found on GitHub.', href='https://github.com/UBC-MDS/DSCI-532_2024_13_Juno', style={'font-size': '14px', 'margin-bottom': '10px'})
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

    # Implementing filtering based on widgets
    # Bug with filtering everything at once - will filter step wise until I find a solution
    geo_filtered_data = card_data[card_data['GEO'] == province_filter]
    industry_filtered_data = geo_filtered_data[geo_filtered_data['Industry'] == industry_filter]
    filtered_data = industry_filtered_data[industry_filtered_data['REF_DATE'] == year_filter]  # Final filter

    women_card_df = filtered_data.query('Gender == "Women"')
    men_card_df = filtered_data.query('Gender == "Men"')
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



# Server side callbacks/reactivity
@app.callback(
    Output('bar2-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    df = pd.read_csv('data/filtered/bar_chart2_data.csv')
    # Filter the DataFrame based on selected year and province
    filtered_df = df[(df["REF_DATE"] == year) & (df["GEO"] == province)]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Industry', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside', marker=dict(color='green')))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside', marker=dict(color='purple')))

    layout = go.Layout(barmode='group', title='Distribution by Industry and Gender', xaxis=dict(title='Industry'), yaxis=dict(title='Count'), width = 600)

    return {'data': data, 'layout': layout}

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
        color = alt.value("#228B22")
    ).properties(
        title='Ratio of Women v/s Men in Executive Positions in {} Over the Years'.format(prov),
        width=1000,
        height=250
    )

    if selected_year is not None:
        rule = alt.Chart(pd.DataFrame({'selected_year': [selected_year]})).mark_rule(color='gray').encode(
            x='selected_year:O'
        ).transform_filter(
            alt.FieldEqualPredicate(field='selected_year', equal=selected_year)
        )
        chart_with_marker = chart + rule
    else:
        chart_with_marker = chart
    
    canada_tot_ratio = alt.Chart(canada_total_ratio).mark_line(strokeDash=[1,1]).encode(
        x='Year:O',
        y='Ratio:Q',
        color = alt.value("#800080")
    )

    chart_with_marker = chart_with_marker + canada_tot_ratio

    return chart_with_marker.configure_axis(
        labelAngle=0
    ).to_dict()

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    df = pd.read_csv('data/filtered/bar_chart_data.csv')
    # Filter the DataFrame based on selected year and province
    filtered_df = df[(df["REF_DATE"] == year) & (df["GEO"] == province)]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Type of corporation', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside', marker=dict(color='green')))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside', marker=dict(color='purple')))

    layout = go.Layout(barmode='group', title='Distribution by Type of corporation and Gender', xaxis=dict(title='Type of corporation'), yaxis=dict(title='Count'), width = 400)

    return {'data': data, 'layout': layout}



# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port = 8052)
