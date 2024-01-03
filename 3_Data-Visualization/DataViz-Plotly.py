# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

#url =  "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#spacex_df = pd.read_csv(url)

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Dropdown menu options
dropdown_options = [
    {'label': 'ALL SITES', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=dropdown_options,
                                            value='ALL',
                                            placeholder="Select Launch Sites",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0: '0',
                                                       5000:'5000',
                                                        10000: '10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launch for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]['class'].value_counts()
        fig = px.pie(filtered_df, values=filtered_df.values, names=filtered_df.index, title=f'Total Success Launch for {entered_site}')

    fig.update_layout(title_x=0.5)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0])
                                  & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        scatter_chart = px.scatter(filtered_data, x="Payload Mass (kg)", y="class",
                                 color="Booster Version Category",
                                   title='Correlation between Payload and Launch Success for All Sites')
    else:
        selected_site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_data = selected_site_data[(selected_site_data['Payload Mass (kg)'] >= payload_range[0]) &
                                           (selected_site_data['Payload Mass (kg)'] <= payload_range[1])]
        scatter_chart = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                            title=f'Correlation between Payload and Launch Success at {selected_site}')
    scatter_chart.update_layout(title_x=0.5)
    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()