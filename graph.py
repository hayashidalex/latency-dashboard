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

    latency_df = pd.read_json(data)
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

    return line_fig
