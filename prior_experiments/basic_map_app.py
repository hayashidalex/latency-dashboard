import pandas as pd
import plotly.graph_objects as go # or plotly.express as px

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

fig.add_trace(
    go.Scattergeo(
        lon = sites_df['lon'],
        lat = sites_df['lat'],
        mode = 'lines',
        line = dict(width = 2,color = 'red'),
        #hovertext=['1-2'],
        #textposition='top center',
    )
)

fig.update_layout(
        title = 'Sites',
        geo_scope='world',
    )

from dash import Dash, dcc, html

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig, style={'width': '90vw', 'height': '90vh'})
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
