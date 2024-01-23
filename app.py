import plotly.graph_objects as go # or plotly.express as px

node_names = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9', 'node10', 'node11', 'node12', 'node13']

ips = ['10.129.129.2', '10.131.1.2', '10.136.129.2', '10.143.2.2', '10.134.129.2', '10.140.132.2', '10.147.1.2', '10.131.129.2', '10.136.1.2', '10.145.3.2', '10.132.133.2', '10.135.130.2', '10.139.130.2', '10.141.1.2']

sites = ['STAR', 'MICH', 'GATECH', 'CERN', 'UCSD', 'PSC', 'HAWI', 'MASS', 'CLEM', 'AMST', 'NCSA', 'FIU', 'PRIN', 'RUTG']

lons = [-88.15754272774885, -83.7101319, -84.3875488, 6.0469869175479545, -117.23932400094392, -79.75279924982625, -157.81639907976145, -72.60787662257826, -82.82128891709674, 4.9558617, -88.24153692109071, -80.37028935316201, -74.61607053887278, -74.4482338]

lats = [42.235998882912895, 42.2931086, 33.7753991, 46.2338702, 32.88868022489132, 40.43394339243079, 21.29897615, 42.202493000000004, 34.586543500000005, 52.3545559, 40.09584003877901, 25.754294805404385, 40.34612035, 40.52489]



fig = go.Figure()

fig.add_trace(go.Scattergeo(
        #lon = df['lon'],
        #lat = df['lat'],
        lon = lons,
        lat = lats,
        #text = df['site_name'] + '; ' + df['exp_ip'],
        text = sites,
        marker=dict(size=8, color="blue")
        ))

fig.add_trace(
    go.Scattergeo(
        lon = lons,
        lat = lats,
        mode = 'lines',
        line = dict(width = 1,color = 'red'),
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
