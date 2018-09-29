import boto3
import botocore
from config import config
import os

Bucket = "makdataset"
Key = "players.zip"

outPutName = os.path.join(config.DATASET_FOLDER, Key)

s3 = boto3.resource('s3', aws_access_key_id="",
                    aws_secret_access_key="", region_name='')
try:
    s3.Bucket(Bucket).download_file(Key, outPutName)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
