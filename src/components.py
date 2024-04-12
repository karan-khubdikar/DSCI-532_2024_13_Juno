from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc


from data import df



title = [html.H1('Juno: Gender Equality in Executive Positions Across Canada'), html.Br()]
province_columns = df['GEO'].unique()#.remove('Unclassified province or territory')
province_columns = province_columns[province_columns!='Unclassified province or territory']
industry_columns = df['Industry'].unique()
time_columns = df['REF_DATE'].unique()


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



line_chart = dvc.Vega(id='line-chart')

barchart = dbc.Col(dcc.Graph(id='bar-chart'))
barchart2 = dbc.Col(dcc.Graph(id='bar2-chart'))


placeholder = html.P(id='placeholder-filter')

map = dvc.Vega(id = "map")