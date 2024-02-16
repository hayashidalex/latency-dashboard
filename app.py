from datetime import datetime
import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px 
import load_data as data_loader
import graph

'''
Requirements
-----------
sites.csv: site, lon, lat (for all sites)
slice.csv: site, ip_address, node_name
data.csv: (downloaded from InfluxDB) latency, received, receiver, sender, seq_n, DateTime

'''

############ Input data ##############

# Create one Dataframe with all the geo-location information
# TODO: use load_data and move this to  after the "Download button" 

sites_df = data_loader.get_geoloc_df()


## Create another Dataframe of latency cada
#latency_df = pd.read_csv("data.csv", header=0, comment="#")
#
## For some reason there is an unwanted column, so delete that
#latency_df.drop('Unnamed: 0', axis=1, inplace=True)
#
## Convert Unix epoch time to datetime64 type
#latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')



############   Layout  #################

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# TODO: Move the style to CSS

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Node 1"),
                dbc.Select(
                    id="src-node",
                    options=[
                        {"label": i, "value": i} for i in sites_df['site'].tolist()
                    ],
                    value="STAR",
                ),
            ],
            style={'marginBottom': 2, 
                    'marginTop': 20, 
                    'marginLeft': 5, 
                    'marginRight':5},
        ),
        html.Div(
            [
                dbc.Label("Node 2"),
                dbc.Select(
                    id="dst-node",
                    options=[
                        {"label": i, "value": i} for i in sites_df['site'].tolist()
                    ],
                    value="STAR",
                ),
            ],
            style={'marginBottom': 2, 
                    'marginTop': 20, 
                    'marginLeft': 5, 
                    'marginRight':5}
        ),
        html.Div(
            [
                dbc.Label("Duration"),
                dbc.Select(
                    id="duration2",
                    options=[
                        {"label": i, "value": i} for i in \
                        ['5 minutes', '15 minutes', '30 minutes', \
                         '1 hour', '3 hours', '6 hours', '12 hours']
                    ],
                    value="5 minutes",
                ),
            ],
            style={'marginBottom': 2, 
                    'marginTop': 20, 
                    'marginLeft': 5, 
                    'marginRight':5}
        ),
        html.Div(
            [
                dbc.Button("Submit", id='submit-button-state', n_clicks=0, outline=True, color="primary"),
            ], 
            style={'marginBottom': 25, 
                    'marginTop': 20, 
                    'marginLeft': 10}
        ),

    ],
)


app.layout = dbc.Container(
    [
        html.H2("FABRIC Latency Monitor"),
        html.Hr(),
        dbc.Row([
            html.Div(
                [
                    dbc.Label("Duration"),
                    dbc.Select(
                        id="duration",
                        options=[
                            {"label": i, "value": i} for i in \
                            ['5 minutes', '15 minutes', '30 minutes', \
                            '1 hour', '3 hours', '6 hours', '12 hours']
                        ],
                        value="5 minutes",
                    ),
                    html.Div(id='download-time')
                ],
            ),
            html.Div(
                [
                    dbc.Button("Download", id='download-button-state', n_clicks=0, outline=True, color="primary"),
                ], 
                style={'marginBottom': 25, 
                        'marginTop': 20, 
                        'marginLeft': 10}
            ),
            ]
        ),
        dbc.Row(
                
            [
                dbc.Col(dcc.Graph(id='map-fig'), lg=8),
                dbc.Col(controls, lg=4),
            ],
            align="center",
        ),
        dbc.Row(dcc.Graph(id='single-latency-fwd')),
        dbc.Row(dcc.Graph(id='single-latency-rev')),
        dcc.Store(id='latency-data')
    ],
    fluid=True,
)


########## Callbacks #########

@callback(
    Output('latency-data', 'data'), 
    Output('download-time', 'children'),
    Input('download-button-state', 'n_clicks'),
    State('duration', 'value'), prevent_initial_call=True)
def download_data(n, duration):
    
    df = data_loader.load_current_latency_csv(duration=duration, 
                                            file_path='./data/data.csv')
    
    msg = f'Data downloaded at {datetime.now()}'

    return df.to_json(), msg


@callback(
    Output('single-latency-fwd', 'figure'),
    Output('single-latency-rev', 'figure'),
    Output('map-fig', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('src-node', 'value'),
    State('dst-node', 'value'),
    State('latency-data', 'data'), prevent_initial_call=True)
def update_figure(n, src, dst, latency_data):
    '''
    Returns two graph figures
    '''
    '''
    #### Line graph  #####
    src_ip = sites_df.loc[sites_df['site'].str.contains(src), 'ip_address'].item()
    dst_ip = sites_df.loc[sites_df['site'].str.contains(dst), 'ip_address'].item()

    #print(f'source {src_ip}, destination {dst_ip}')
    
    latency_df = pd.read_json(latency_data)
    latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')


    selected_df = latency_df[latency_df['receiver'].str.contains(dst_ip) & \
                         latency_df['sender'].str.contains(src_ip)]

    title = f'{src} ({src_ip}) --> {dst} ({dst_ip}) \n One-way Latency (GMT)'
    line_fig = px.line(selected_df, 
                x="received",
                y="latency",
                title=title,
                labels = {"received": "Probe Packet Arrival Time (GMT)",
                          "latency": "Latency (M = milliseconds)"}
                )
    '''
    line_fig_fwd = graph.generate_line_graph(src, dst, latency_data)
    line_fig_rev = graph.generate_line_graph(dst, src, latency_data)

    #####  Map graph ######
    map_fig = go.Figure()

    map_fig.add_trace(go.Scattergeo(
            name = "FABRIC sites",
            lon = sites_df['lon'],
            lat = sites_df['lat'],
            text = sites_df['site'] + '; ' + sites_df['ip_address'],
            marker=dict(size=8, color="blue")
            ))
   
    
    # Add a line between src and dst

    src_lon = sites_df.loc[sites_df['site'].str.contains(src), 'lon'].item()
    src_lat = sites_df.loc[sites_df['site'].str.contains(src), 'lat'].item()
    dst_lon = sites_df.loc[sites_df['site'].str.contains(dst), 'lon'].item()
    dst_lat = sites_df.loc[sites_df['site'].str.contains(dst), 'lat'].item()
    
    map_fig.add_trace(
        go.Scattergeo(
            name = "path",
            lon = [src_lon, dst_lon],
            lat = [src_lat, dst_lat],
            mode = 'lines',
            line = dict(width = 2,color = 'red'),
        )
    )
    
    map_fig.update_geos(
        lataxis_range=[-30,80],
        lonaxis_range=[-250,50]
        )
    
    map_fig.update_layout(
            title = 'FABRIC slice sites',
        )
    
    return line_fig_fwd, line_fig_rev, map_fig



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  

    # If running on a remote node    
    #app.run_server(host='0.0.0.0',debug=False, use_reloader=False)
