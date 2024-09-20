from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# for local server version

bucket = "my-bucket"
client = InfluxDBClient(url="https://adddress:<port>", 
    token="<token>", 
    org="fabric")

query_api = client.query_api()


## using Table structure. TODO: it retrieves 3 fields as separate data points

query = """from(bucket: "owl")
  |> range(start: -20m)
  |> filter(fn: (r) => r["_measurement"] == "owl")
  |> filter(fn: (r) => r["_field"] == "latency" or r["_field"] == "seq_n" or r["_field"] == "received")
  |> filter(fn: (r) => r["receiver"] == "10.129.147.2")
  |> filter(fn: (r) => r["sender"] == "10.131.131.2")"""

tables = query_api.query(query)

for table in tables:
    print(table)
    for row in table.records:
        print (row.values)

# Convert pyarrow.Table to values (TODO: debug this)
latency_values = tables.to_values(columns = ['received', 'latency', 'seq_n', 'receiver', 'sender'])

print(latency_values)
