import os, time
from influxdb_client_3 import InfluxDBClient3, Point

# For cloud InfluxDB 


host =  "<host url (may need to include :port)"
org = "<org>"
database = "<bucket name>"
token = "<token>"

client = InfluxDBClient3(host=host, token=token, org=org)


query = """SELECT *
FROM "owl"
WHERE
time >= now() - interval '10 minutes'
AND
("latency" IS NOT NULL OR "received" IS NOT NULL)"""

table = client.query(query=query, 
                    database="owl", 
                    language="sql", mode="all")

print("table:")
print(table)

#from pyarrow import csv
#
#write_options = csv.WriteOptions(include_header=False)
#csv.write_csv(table, "test.csv", write_options=write_options )

