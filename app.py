import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

# Still hard-coded 
# Will receive this from the slice (somehow)

node_names = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9', 'node10', 'node11', 'node12', 'node13']

ips = ['10.129.129.2', '10.131.1.2', '10.136.129.2', '10.143.2.2', '10.134.129.2', '10.140.132.2', '10.147.1.2', '10.131.129.2', '10.136.1.2', '10.145.3.2', '10.132.133.2', '10.135.130.2', '10.139.130.2', '10.141.1.2']

sites = ['STAR', 'MICH', 'GATECH', 'CERN', 'UCSD', 'PSC', 'HAWI', 'MASS', 'CLEM', 'AMST', 'NCSA', 'FIU', 'PRIN', 'RUTG']

# Create a Dataframe with all relevant information

locs_df = pd.read_csv('sites.csv')
sites_df = pd.DataFrame(sites, columns=['site'])
sites_df = sites_df.merge(locs_df)
sites_df.insert(0, 'node_name', node_names)
sites_df.insert(1, 'ip_address', ips)


# Create map

fig = go.Figure()

fig.add_trace(go.Scattergeo(
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

fig.update_geos(
    #center=dict(lon=0, lat=-80),
    lataxis_range=[-30,80],
    lonaxis_range=[-250,50]
    )

fig.update_layout(
        title = 'Sites',
        #geo_scope='world',
    )

# Callback + line graph
#TODO




# Layout

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                        {"label": i, "value": i} for i in sites_df['site'].tolist() 
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
                dbc.Label("Duration in Minutes"),
                dbc.Input(id="min", type="number", value=10),
            ],
            style={'marginBottom': 2, 
                    'marginTop': 20, 
                    'marginLeft': 5, 
                    'marginRight':5}
        ),
        html.Div(
            [
                dbc.Button("Submit", outline=True, color="primary"),
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
                dbc.Col(dcc.Graph(figure=fig), lg=8),
                dbc.Col(controls, lg=4),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  
    # Turn off reloader if inside Jupyter
