# Exporting Redis Data to S3 as CSV using Python and boto3

This Python script connects to an Amazon ElastiCache for Redis cluster and exports its data to an Amazon S3 bucket as CSV files.

## Prerequisites

### 1. **Create a Redis Cluster:**

- Click on "Create" to create a new ElastiCache cluster.
    - Choose "Redis" as the engine.
    - Select the desired Redis engine version.
    - Choose the cluster mode. For simplicity, you can start with a replication group.
    - Configure settings like the cluster name, node type, number of replicas, etc.
    - Choose the appropriate network settings (VPC, Subnet Group).
    - Configure security group settings (make sure your Redis cluster is accessible from where it's needed but still secure).


 ![Screenshot from 2024-04-28 11-15-47](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/bc88bf29-c2ef-4997-bcc3-c08fd1eba4a3)


### 2. **Launch Ubuntu Server to Access Cluster:**

 ![Screenshot from 2024-04-28 11-21-33](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/5fb84a80-3f0a-4f84-9f2d-5e36d44d77ff)


### 3. **Installing and Configuring Redis:**

  ```bash
    sudo apt update -y
    sudo apt install redis-server
    sudo systemctl status redis
  ```
   ![Screenshot from 2024-04-28 11-27-53](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/e12d1b70-8af8-4f59-8a08-e4d743c4737d)


### 4. **Accessing Your Redis Cluster:**
    - Once the cluster is created, note down the endpoint address.
    - Use this endpoint to connect to your Redis cluster from your application code.

   ![Screenshot from 2024-04-28 11-31-07](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/b2b6355a-2e82-44fd-91b3-4b7035049edb)

### 5. **Create S3 Bucket:**

   ![Screenshot from 2024-04-28 12-28-51](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/c79e3782-131a-481b-894e-78148f43cdc8)


### 6. **create a Python environment:**

To create a Python environment, you can use virtual environments, which allow you to create isolated Python environments for your projects. Here's how you can create a Python environment using virtualenv:

```bash
   pip install virtualenv
   sudo apt install python3-virtualenv
   virtualenv myenv
   source myenv/bin/activate
```

![Screenshot from 2024-04-28 12-16-06](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/ea34c641-58a4-467c-a315-69324482b65a)


### 7.  Running the Python Script:


1. Make sure you have Python and boto3 installed.

![Screenshot from 2024-04-28 12-19-03](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/a5ce078d-f5c2-46c8-a77d-e623f1df99b5)

2. Install redis `pip3 install redis`

![Screenshot from 2024-04-28 12-23-20](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/d6004af8-0585-49e8-a759-00b03034c8f3)


3. Create a file like `python.py` and Upload this script in it.

```bash 
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

```

4. Replace `'REDIS_ENDPOINT'`, `'S3_BUCKET_NAME'`, and `'S3_KEY'` in the script with your actual Redis endpoint, S3 bucket name, and S3 key prefix, respectively.


5. Run the script.

```bash
   python3 python.py
```

![Screenshot from 2024-04-28 12-41-30](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/80ae737e-64c8-45d6-aa0f-2e64c3ce0ee9)


6. Check whether the data is stored in the s3 bucket or not.

![Screenshot from 2024-04-28 12-43-07](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/eea73836-8e63-449b-bb40-bb555da4ef39)


![Screenshot from 2024-04-28 12-44-24](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/61d80d6e-4c45-45a8-81fe-62b521ced7e9)


7. Data stored in CSV form

![Screenshot from 2024-04-28 12-45-42](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/216ab496-3182-46fe-9717-5a7725894366)



#### Script Explanation

1. Connects to the ElastiCache Redis cluster.
2. Retrieves all keys and values from the Redis cluster.
3. Writes the data to a CSV file.
4. Uploads the CSV file to an Amazon S3 bucket.
