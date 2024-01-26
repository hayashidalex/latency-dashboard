# latency-dashboard

## Purpose

A simple demo to view [FABRIC Measurement Framework OWL](
https://github.com/fabric-testbed/MeasurementFramework/tree/main/user_services/owl)
data using a csv file downloaded from InfluxDB and 2 other resource information
files.

## Usage

```
# First time only
python3 -m venv venv


source venv/bin/activate

# If necesssary
pip install -r requirements.txt

python app.py
```

Then, connect to `http://127.0.0.1:8050/`


## Required Files

- `data.csv`: CSV file downloaded from InfluxDB
- `sites.csv`: FABRIC sites latitudes and longitudes
- `slice.csv`: Information on the FABRIC slice used for this data collection

### Format
```
==> data.csv <==
#group,false,false,false,false,false,false
#datatype,long,double,string,string,long,dateTime:RFC3339
#default,,,,,,
,latency,received,receiver,sender,seq_n,time
,2677604,1706000181.561673,10.129.129.2,10.131.1.2,1531,2024-01-23T08:56:21.558995396Z
,2673063,1706000241.561918,10.129.129.2,10.131.1.2,1532,2024-01-23T08:57:21.559244937Z
,2677987,1706000301.562251,10.129.129.2,10.131.1.2,1533,2024-01-23T08:58:21.559573013Z
,2663712,1706000361.562549,10.129.129.2,10.131.1.2,1534,2024-01-23T08:59:21.559885288Z
,2665076,1706000421.562836,10.129.129.2,10.131.1.2,1535,2024-01-23T09:00:21.560170924Z
,2680888,1706000481.563096,10.129.129.2,10.131.1.2,1536,2024-01-23T09:01:21.560415112Z

==> sites.csv <==
site,lat,lon
HAWI,21.29897615,-157.81639907976145
EDUKY,38.0325,-84.502801
GATECH,33.7753991,-84.3875488
NEWY,40.7383575,-73.9992012

==> slice.csv <==
site,node_name,ip_address
STAR,node0,10.129.129.2
MICH,node1,10.131.1.2
GATECH,node2,10.136.129.2
CERN,node3,10.143.2.2
```
