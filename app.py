import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px 

# Still hard-coded 
# TODO: Will receive this from the slice (somehow)

node_names = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9', 'node10', 'node11', 'node12', 'node13']

ips = ['10.129.129.2', '10.131.1.2', '10.136.129.2', '10.143.2.2', '10.134.129.2', '10.140.132.2', '10.147.1.2', '10.131.129.2', '10.136.1.2', '10.145.3.2', '10.132.133.2', '10.135.130.2', '10.139.130.2', '10.141.1.2']

sites = ['STAR', 'MICH', 'GATECH', 'CERN', 'UCSD', 'PSC', 'HAWI', 'MASS', 'CLEM', 'AMST', 'NCSA', 'FIU', 'PRIN', 'RUTG']

# Create one Dataframe with all the geo-location information

locs_df = pd.read_csv('sites.csv')
sites_df = pd.DataFrame(sites, columns=['site'])
sites_df = sites_df.merge(locs_df)
sites_df.insert(0, 'node_name', node_names)
sites_df.insert(1, 'ip_address', ips)


# Create another Dataframe of latency cada
# For some reason there is an unwanted column, so delete that
latency_df = pd.read_csv("sample.csv", header=0, comment="#")
latency_df.drop('Unnamed: 0', axis=1, inplace=True)


###############  Create map  ###########

map_fig = go.Figure()

map_fig.add_trace(go.Scattergeo(
        lon = sites_df['lon'],
        lat = sites_df['lat'],
        text = sites_df['site'] + '; ' + sites_df['ip_address'],
        marker=dict(size=8, color="blue")
        ))

#fig.add_trace(
#    go.Scattergeo(
#        lon = sites_df['lon'],
#        lat = sites_df['lat'],
#        mode = 'lines',
#        line = dict(width = 2,color = 'red'),
#        #hovertext=['1-2'],
#        #textposition='top center',
#    )
#)

map_fig.update_geos(
    #center=dict(lon=0, lat=-80),
    lataxis_range=[-30,80],
    lonaxis_range=[-250,50]
    )

map_fig.update_layout(
        title = 'Sites',
        #geo_scope='world',
    )

# TODO: Either add a line or change the color of the src and dst


######## Layout

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
                        {"label": i, "value": j} \
                         for i, j in zip(sites_df['site'].tolist(), sites_df['ip_address'].tolist())
                    ],
                    value="10.0.0.1",
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
                        {"label": i, "value": j} \
                         for i, j in zip(sites_df['site'].tolist(), sites_df['ip_address'].tolist())
                    ],
                    value="10.0.1.1",
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
                dbc.Col(dcc.Graph(figure=map_fig), lg=8),
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
    Input('submit-button-state', 'n_clicks'),
    State('src-node', 'value'),
    State('dst-node', 'value')
    )
def update_figure(n, src, dst):
    selected_df = latency_df[latency_df['receiver'].str.contains(dst) & \
                         latency_df['sender'].str.contains(src)]

    line_fig = px.line(selected_df, x="received", y="latency",
                title=f'{src} --> {dst} Latency (TODO: change to site names)')

    return line_fig



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  
    # Turn off reloader if inside Jupyter
