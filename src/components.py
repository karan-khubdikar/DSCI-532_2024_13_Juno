from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

from data import df

title = [html.H1('Juno: Gender Equality in Executive Positions Across Canada'), html.Br()]
dataset_description = [html.P('A note on the data: As the dataset we is limited, data is not available for some subsets and territories (like Nunavut). If your subset is turning out blank charts, this could be why. The charts will also be blank if you clear all filters',  style={'font-size': '14px'}), html.Br()]
project_description = [
    html.P(
        "This project scrutinizes the gender disparity in top-level leadership roles within Canadian corporations across multiple sectors. Leveraging gender-disaggregated data, we aim to reveal the potential influence of gender balance in decision-making roles on more effective and inclusive policies. The displayed dashboards are filtered based on the selected tags, showing only those that match all selected tags. Tag counts are updated dynamically to reflect the number of visible dashboards after filtering. For optimal viewing, this dashboard is recommended for a full-width window.",
        style={'font-size': '16px'}
    ),
    html.Br(),
    html.P(
        "Ancient Romans worshipped Juno as the queen of the gods, the female counterpart to the chief of the gods, Jupiter. Since our app looks at the gender makeup of the top-level management in companies across Canada, we felt that Juno, as the CEO/COO equivalent of the Roman pantheon, would be a good representation of the female leaders we are highlighting in our data set. Furthermore, Juno's close association with women and her status as the protector of women resonates with our more aspirational goal, which is to uncover potential areas for improving inclusivity and gender equality in Canadian corporations. As a champion of women, and a prominent female leader herself, we feel that Juno is a good symbol of what we strive to achieve with this app. We have thus named our app after her.",
        style={'font-size': '16px'}
    )
]
juno_explanation = [html.P("Ancient Romans worshipped Juno as the queen of the gods, the female counterpart to the chief of the gods, Jupiter. Since our app looks at the gender makeup of the top-level management in companies across Canada, we felt that Juno, as the CEO/COO equivalent of the Roman pantheon, would be a good representation of the female leaders we are highlighting in our data set. Furthermore, Juno's close association with women and her status as the protector of women resonates with our more aspirational goal, which is to uncover potential areas for improving inclusivity and gender equality in Canadian corporations. As a champion of women, and a prominent female leader herself, we feel that Juno is a good symbol of what we strive to achieve with this app. We have thus named our app after her.", style={'font-size': '16px'})]

collapse_button = dbc.Button(
    "What is Juno?",
    id="collapse-button",
    outline=False,
    style={
        'width': '150px',
        'background-color': 'white',
        'color': 'steelblue',
        'margin-top': 10,
    }
)

collapse_section = dbc.Collapse(
        project_description,
    id="collapse",
)

province_columns = df['GEO'].unique()
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
card_ratio = dbc.Card(id='card-ratio')


industry = dcc.Dropdown(id='industry-filter', options=industry_columns, value='Total all industries'),



line_chart = dvc.Vega(id='line-chart')

barchart = dbc.Col(dcc.Graph(id='bar-chart'))
barchart2 = dbc.Col(dcc.Graph(id='bar2-chart'))


placeholder = html.P(id='placeholder-filter')

map = dvc.Vega(id = "map")