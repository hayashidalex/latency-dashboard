from datetime import datetime                                                      
import pandas as pd                                                                
import plotly.graph_objects as go # or plotly.express as px                        
import dash_bootstrap_components as dbc                                            
from dash import Dash, dcc, html, Input, Output, State, callback                   
import plotly.express as px                                                        
import load_data as data_loader                                                    
                                    

sites_df = data_loader.get_geoloc_df()

def generate_line_graph(src, dst, data):

    src_ip = sites_df.loc[sites_df['site'].str.contains(src), 'ip_address'].item()
    dst_ip = sites_df.loc[sites_df['site'].str.contains(dst), 'ip_address'].item()

    #latency_df = pd.read_json(data)
    #latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')


    selected_df = data[data['receiver'].str.contains(dst_ip) & \
                        data['sender'].str.contains(src_ip)]
    
    selected_df.sort_values(by="received", inplace=True)


    title = f'{src} ({src_ip}) --> {dst} ({dst_ip}) \n One-way Latency (GMT)'
    line_fig = px.line(selected_df,
                x="received",
                y="latency",
                title=title,
                labels = {"received": "Probe Packet Arrival Time (GMT)",
                          "latency": "Latency (M = milliseconds)"}
                )

    return line_fig


def generate_map(src, dst):
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

    return map_fig
