import pandas as pd
import geopandas as gpd


df = pd.read_csv("data/raw/filtered_canada.csv")

new_df = df[(df["Size of enterprise"] == "Total all sizes") &
            (df["Unit of measure"] == "Number") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Unclassified province or territory")&
            (df["Industry"] != "")
].copy()
new_df = new_df.loc[:, ["REF_DATE", "Gender", "GEO", "VALUE", "Industry", "Type of corporation"]]

replacement_dict = {'Government business entities': 'Government', 
                    'Publicly traded corporations': 'Public', 
                    'Private enterprises': 'Private', 
                    'Unclassified enterprises': 'Unclassified',
                    'Total all corporations': 'Total'}

replacement_df = new_df.copy()
replacement_df['Type of corporation'] = replacement_df['Type of corporation'].map(replacement_dict)


replacement_dict_2 = {'Finance': 'Finance', 
                    'Utilities': 'Utilities', 
                    'Management of companies and enterprises': 'Management', 
                    'Distributive trade': 'Distributive trade',
                    'Total all industries': 'Total',
                    'Energy':'Energy',
                    'Manufacturing':'Manufacturing',
                    'Construction':'Construction',
                    'Other industry':'Other',
                    'Unclassified industry':'Other'}

replacement_df['Industry'] = replacement_df['Industry'].map(replacement_dict_2)

replacement_df.to_csv('data/filtered/filtered_data_replaced.csv', index=False)

new_df.to_csv('data/filtered/filtered_data.csv', index=False)

df = pd.read_csv('data/filtered/filtered_data.csv')

canadian_provinces = gpd.read_file('data/filtered/map_chart_data.geojson')
