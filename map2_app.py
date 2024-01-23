import plotly.graph_objects as go # or plotly.express as px

fig = go.Figure()

fig.add_trace(go.Scattergeo(
        #lon = df['lon'],
        #lat = df['lat'],
        lon = [10, 20, 30],
        lat = [10, 20, 30],
        #text = df['site_name'] + '; ' + df['exp_ip'],
        text = ['1', '2', '3'],
        marker=dict(size=8, color="blue")
        ))

fig.add_trace(
    go.Scattergeo(
        lon = [10, 20],
        lat = [10, 20],
        mode = 'lines',
        line = dict(width = 1,color = 'red'),
        hovertext=['1-2'],
        textposition='top center',
    )
)

fig.update_layout(
        title = 'Slice nodes',
        geo_scope='world',
    )

from dash import Dash, dcc, html

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig, style={'width': '90vh', 'height': '90vh'})
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
