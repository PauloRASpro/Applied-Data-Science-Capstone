# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 10:34:21 2023

@author: CDB7
"""

# Import required libraries
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div([html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)                                
                                dcc.Dropdown(   
                                            id='site-dropdown',  
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ], 
                                                value='ALL', 
                                                placeholder='Select Site', 
                                                searchable=True
                                ),  
                                html.Br(),                                

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={ int(min_payload): str(min_payload) ,
                                                        int(max_payload): str(max_payload)} ,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site): 
    print(entered_site)
    if entered_site == 'ALL':
        data = spacex_df [ (spacex_df['class'] == 1) ]
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launch By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data = spacex_df[ (spacex_df['Launch Site'] == entered_site) ]  
        len_data1 = len(data[ (data['class'] == 1) ])
        len_data0 = len(data[ (data['class'] == 0) ])        
        data_dict = {'num_class':[len_data0, len_data1], 'status': ['Success', 'Failure']}
        data_f=pd.DataFrame(data_dict)
        fig = px.pie(data_f, values='num_class', names='status', title=f'Total Success Launch for Site {entered_site}')
        return fig 
        


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter(entered_site, payload_value):
    # Select data    
    print(entered_site, payload_value)
    if entered_site == 'ALL':
        df =  spacex_df[ (spacex_df['Payload Mass (kg)'] >= payload_value[0]) & 
                         (spacex_df['Payload Mass (kg)'] <= payload_value[1]) ]       
                      
        
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        
        fig.update_layout(title='Correlation of Payload Mass (kg) vs Class for ALL sites', xaxis_title='Payload Mass (kg)', yaxis_title='Class') 
        
        return fig      
    
    else:
        df =  spacex_df[ (spacex_df['Launch Site'] == entered_site) & 
                         (spacex_df['Payload Mass (kg)'] >= payload_value[0]) & 
                         (spacex_df['Payload Mass (kg)'] <= payload_value[1]) ]    
        
       
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        
        fig.update_layout(title=f'Correlation of Payload Mass (kg) vs Class for site {entered_site}', xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        
        return fig


# Run the app at http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run_server()
    