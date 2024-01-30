import pandas as pd
import configparser
from influxdb_client_3 import InfluxDBClient3, Point
from pyarrow import csv

'''
Requirements
-----------
sites.csv: site, lon, lat (for all sites)
slice.csv: site, ip_address, node_name
data.csv: (downloaded from InfluxDB) latency, received, receiver, sender, seq_n, DateTime

'''

def get_geoloc_df(sites_file='./data/sites.csv', slice_file='./data/slice.csv'):
    all_sites_df = pd.read_csv('./data/sites.csv')
    slice_df = pd.read_csv('./data/slice.csv')
    slice_df = slice_df.merge(all_sites_df)
    
    return slice_df


def load_manually_downloaded_csv(file_path='./data/downloaded_data.csv'):

    latency_df = pd.read_csv(file_path, header=0, comment="#") 

    # For some reason there is an unwanted column when manually downloaded.
    # Delete that.
    latency_df.drop('Unnamed: 0', axis=1, inplace=True)

    # Convert Unix epoch time to datetime64 type
    latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')
    
    return latency_df


def load_current_latency_csv(duration='15 minute', file_path='./data/data.csv'):

    '''
    Return latency data as Pandas Dataframe. 
    If file_path (str) is given, table will use the saved csv file.
    Otherwise, download the latest data from InfluxDB
    '''

    _download_influx_data(duration=duration, outfile=file_path)

    # Create Dataframe of latency data and add column names
    latency_df = pd.read_csv(file_path, header=0, comment="#",
                names=["latency","received","receiver","sender","seq_n","time"])    

   
    # Convert Unix epoch time to datetime64 type
    #latency_df['received'] = pd.to_datetime(latency_df['received'], unit='s')

    return latency_df



def _download_influx_data(duration='15 minute', outfile='./data/data.csv'):
    '''
    duration(str): '1 minute', '5 minutes', '3 hours', '2 days' etc.
    '''

    # Read InfluxDB conf
    config = configparser.ConfigParser()
    config.read('influxdb.conf')
    
    host = config['InfluxDB']['host']
    token = config['InfluxDB']['token']
    org = config['InfluxDB']['org']
    database = config['InfluxDB']['database']
    language = config['InfluxDB']['language']

    #print(f'host {host}, token: {token}, org: {org}, database: {database}, \
    #    language: {language}')

    client = InfluxDBClient3(host=host, token=token, org=org)
        
    query = """SELECT *
    FROM "owl"
    WHERE
    time >= now() - interval '{duration}'
    AND
    ("latency" IS NOT NULL OR "received" IS NOT NULL)""".format(
    duration=duration)
    
    table = client.query(query=query, 
                        database=database, 
                        language=language, mode="all")
    
    
    write_options = csv.WriteOptions(include_header=False)
    csv.write_csv(table, outfile, write_options=write_options )


