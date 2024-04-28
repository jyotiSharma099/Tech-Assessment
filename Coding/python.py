import csv
import json
import redis
import boto3
from io import StringIO

# Replace these variables with your own values
REDIS_ENDPOINT = "rediscluster.z3vbct.ng.0001.use1.cache.amazonaws.com"
REDIS_PORT = 6379
S3_BUCKET_NAME = "elasticachestored8888"
S3_KEY = "redis_data"

# Connect to Redis
r = redis.Redis(host=REDIS_ENDPOINT, port=REDIS_PORT)

# Get the keys from Redis
keys = r.keys("*")

# Create a list to store the data
data = []

# Iterate through the keys and get the values
for key in keys:
    value = r.get(key)
    data.append({key.decode('utf-8'): value})

# Create a set to store all unique keys from Redis
all_keys = set()

# Iterate through the keys and get the values
for key in keys:
    value = r.get(key)
    all_keys.add(key.decode('utf-8'))

# Create a list of all unique keys
fieldnames = list(all_keys)

# Create a StringIO object for the CSV data
csv_data = StringIO()

# Create a CSV writer
writer = csv.DictWriter(csv_data, fieldnames=fieldnames)

# Write the header
writer.writeheader()

# Write the data
for row in data:
    # Ensure each dictionary has all the fieldnames
    row_dict = {k: row.get(k) for k in fieldnames}
    writer.writerow(row_dict)

# Get a reference to the S3 client
s3 = boto3.client("s3")

# Write the CSV data to S3
s3.put_object(Bucket=S3_BUCKET_NAME, Key=S3_KEY, Body=csv_data.getvalue(), ContentType="text/csv")
