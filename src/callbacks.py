import altair as alt
import pandas as pd
import plotly.graph_objs as go
from dash import Output, Input, callback
import dash_bootstrap_components as dbc

import geopandas as gpd
# Adding new components in a new line so it is easier to isolate anything new which might be causing problems
from dash import State

from data import df
from data import canadian_provinces
from data import replacement_df

### Make the map of Canada

# Plotting the map of Canada and the 

@callback(
    Output('map', 'spec'),
    Input('year-filter', 'value'),
)
def combined_chart(year_filter):
    map_data = canadian_provinces[canadian_provinces['REF_DATE']==year_filter]
    hover = alt.selection_point(fields=['name'], on='pointerover', empty=False)
    map_chart = alt.Chart(map_data, width= 800, height=600).mark_geoshape(stroke='white').project(
        'transverseMercator',
        rotate=[90, 0, 0]
    ).encode(
        tooltip=['name','Women_to_Men_Ratio'],
        color=alt.Color('Women_to_Men_Ratio', 
                        scale=alt.Scale(domain=[0, 1], 
                                        scheme='viridis'), 
                        title='Proportion of Women'),
        stroke=alt.condition(hover, alt.value('white'), alt.value('#222222')),  # If hovering, stroke white, otherwise black
        order=alt.condition(hover, alt.value(1), alt.value(0))  # Show the hovered stroke on top
    ).add_params(
        hover
    )

    labels = alt.Chart(map_data).mark_text().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        text='postal',
        size=alt.value(15),
        opacity=alt.value(1),
    )
    combined_chart = (map_chart+labels).properties(
        title = "Overall Proportion Across Provinces",
    ).configure_legend(
        orient='top'
    ).configure_title(
    fontSize=25  
)
    combined_chart = combined_chart
    return combined_chart.to_dict()


#Calculate proportions for cards
# Server side callbacks/reactivity
@callback(
    Output('card-women', 'children'),
    Output('card-men', 'children'),
    Output('card-ratio', 'children'),
    Input('province-filter', 'value'),
    Input('industry-filter', 'value'),
    Input('year-filter', 'value'),
)
def calculate_proportion(province_filter, industry_filter, year_filter):

    # Implementing filtering based on widgets
    # Bug with filtering everything at once - will filter step wise until I find a solution
    geo_filtered_data = df[df['GEO'] == province_filter]
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
    card_ratio_content = [
        dbc.CardHeader('Overall Ratio of Women to Men in this Subset'),
        dbc.CardBody(f'{round(prop_women / prop_men, 2)}')
    ]
    
    return card_women_content, card_men_content, card_ratio_content


# Industry bar chart
# Server side callbacks/reactivity
@callback(
    Output('bar2-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    # Filter the DataFrame based on selected year and province
    filtered_df = replacement_df[(replacement_df["REF_DATE"] == year) & (replacement_df["GEO"] == province) & (replacement_df["Industry"]!= "Total")]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Industry', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside', marker=dict(color='green')))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside', marker=dict(color='purple')))

    layout = go.Layout(barmode='group', title='<b>Distribution by Industry and Gender<b>', xaxis=dict(title='Type of Industry'), yaxis=dict(title='Count'), legend=dict(x=0.5, y=1.1, orientation='h'))

    return {'data': data, 'layout': layout}

# Line chart
@callback(
    Output('line-chart', 'spec'),
    [Input('province-filter', 'value'),
     Input('year-filter', 'value')]
)
def create_chart(prov, selected_year):

    filtered_df =df[(df["GEO"] == prov) & (df['Industry'] == 'Total all industries') & (df['Type of corporation'] == 'Total all corporations')]

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
        tooltip=['Ratio:Q'],
        color = alt.value("#228B22")
    ).properties(
        title='Ratio of Women v/s Men in Executive Positions in {} Over the Years'.format(prov),
        width=1200,
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

    text_data = pd.DataFrame({'Year': [2017], 'Ratio': [0.424134], 'label': ['National Average']})
    text = alt.Chart(text_data).mark_text(
        align='left', baseline='middle',
        dx=3 ,
        dy=-7
    ).encode(
        x='Year:O',
        y='Ratio:Q',
        text='label'
    )

    chart_with_marker = (chart_with_marker + canada_tot_ratio + text).configure_legend(
        orient='right'
    )

    return chart_with_marker.configure_axis(
        labelAngle=0
    ).to_dict()

# Corporation bar chart
@callback(
    Output('bar-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    # Filter the DataFrame based on selected year and province
    filtered_df = replacement_df[(replacement_df["REF_DATE"] == year) & (replacement_df["GEO"] == province) & (replacement_df["Type of corporation"] != "Total")]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Type of corporation', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside', marker=dict(color='green')))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside', marker=dict(color='purple')))

    layout = go.Layout(barmode='group', title='<b>Distribution by Type of corporation and Gender<b>', xaxis=dict(title='Type of corporation'), yaxis=dict(title='Count'), legend=dict(x=0.5, y=1.1, orientation='h'))

    return {'data': data, 'layout': layout}

# Dropdown button for information
@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],  # Pass the current "state" of the component (is it open or not)
)
def toggle_collapse(n, is_open):
    print(n)  # The number of times the button has been clicked
    print(is_open)  # Whether the collapse is open or not
    if n:
        return not is_open
    return is_open