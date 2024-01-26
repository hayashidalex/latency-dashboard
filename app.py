import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px 

'''
Requirements
-----------
sites.csv: site, lon, lat (for all sites)
slice.csv: site, ip_address, node_name
sample.csv: (downloaded from InfluxDB) latency, received, receiver, sender, seq_n, DateTime

'''

############ Input data ##############

# Create one Dataframe with all the geo-location information
# TODO This should probably be a separate function or module

locs_df = pd.read_csv('sites.csv')
sites_df = pd.read_csv('slice.csv')
sites_df = sites_df.merge(locs_df)


# Create another Dataframe of latency cada
latency_df = pd.read_csv("sample.csv", header=0, comment="#")

# For some reason there is an unwanted column, so delete that
latency_df.drop('Unnamed: 0', axis=1, inplace=True)

# Convert Unix epoch time to datetime64 type
latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')



############   Layout  #################

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# TODO: Move the style to CSS

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Source Node"),
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
                dbc.Label("Destination Node"),
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
                dbc.Label("Duration (not yet implemented)"),
                dbc.Input(id="min", type="number", value=10),
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
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='map-fig'), lg=8),
                dbc.Col(controls, lg=4),
            ],
            align="center",
        ),
        dbc.Row(dcc.Graph(id='single-latency'))
    ],
    fluid=True,
)


########## Callbacks #########

@callback(
    Output('single-latency', 'figure'),
    Output('map-fig', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('src-node', 'value'),
    State('dst-node', 'value')
    )
def update_figure(n, src, dst):
    '''
    Returns two graph figures
    '''

    #### Line graph  #####
    src_ip = sites_df.loc[sites_df['site'].str.contains(src), 'ip_address'].item()
    dst_ip = sites_df.loc[sites_df['site'].str.contains(dst), 'ip_address'].item()

    #print(f'source {src_ip}, destination {dst_ip}')

    selected_df = latency_df[latency_df['receiver'].str.contains(dst_ip) & \
                         latency_df['sender'].str.contains(src_ip)]

    line_fig = px.line(selected_df, x="received", y="latency",
                title=f'{src} ({src_ip}) --> {dst} ({dst_ip}) Latency in milliseconds')


    #####  Map graph ######
    map_fig = go.Figure()

    map_fig.add_trace(go.Scattergeo(
            lon = sites_df['lon'],
            lat = sites_df['lat'],
            text = sites_df['site'] + '; ' + sites_df['ip_address'],
            marker=dict(size=8, color="blue")
            ))
   
    
    if n > 0:
        # Add a line between src and dst

        src_lon = sites_df.loc[sites_df['site'].str.contains(src), 'lon'].item()
        src_lat = sites_df.loc[sites_df['site'].str.contains(src), 'lat'].item()
        dst_lon = sites_df.loc[sites_df['site'].str.contains(dst), 'lon'].item()
        dst_lat = sites_df.loc[sites_df['site'].str.contains(dst), 'lat'].item()
        
        map_fig.add_trace(
            go.Scattergeo(
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
    
    return line_fig, map_fig



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  
    # Turn off reloader if inside Jupyter
