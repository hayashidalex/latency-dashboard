import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
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

sites_df = data_loader.get_geoloc_df()


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
                         '1 hour', '3 hours', '6 hours', '12 hours', '24 hours']
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
                dbc.Button("Submit", id='submit-button-state', 
                            n_clicks=0, outline=True, color="primary"),
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
        dbc.Row(dcc.Graph(id='single-latency-fwd')),
        dbc.Row(dcc.Graph(id='single-latency-rev')),
    ],
    fluid=True,
)


########## Callbacks #########


@callback(
    Output('single-latency-fwd', 'figure'),
    Output('single-latency-rev', 'figure'),
    Output('map-fig', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('src-node', 'value'),
    State('dst-node', 'value'), 
    State('duration2', 'value'), prevent_initial_call=True)
def update_figure(n, src, dst, duration):
    '''
    Returns 3  graph figures
    '''
    #### Line graphs #####
    src_ip = sites_df.loc[sites_df['site'].str.contains(src), 'ip_address'].item()
    dst_ip = sites_df.loc[sites_df['site'].str.contains(dst), 'ip_address'].item()


    latency_fwd = data_loader.download_influx_data(duration=duration, outfile=None,
            src_dst=(src_ip, dst_ip))
    line_fig_fwd = graph.generate_line_graph(src, dst, latency_fwd)

    latency_rev = data_loader.download_influx_data(duration=duration, outfile=None,
            src_dst=(dst_ip, src_ip))
    line_fig_rev = graph.generate_line_graph(dst, src, latency_rev)

    #####  Map graph ######
    map_fig = graph.generate_map(src, dst)

    return line_fig_fwd, line_fig_rev, map_fig



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  

    # If running on a remote node    
    #app.run_server(host='0.0.0.0',debug=False, use_reloader=False)
