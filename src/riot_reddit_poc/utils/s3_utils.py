import json
import gzip
import io
import boto3
from botocore.exceptions import ClientError


def get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION):
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

def put_ndjson_gz(bucket, key, records_bytes, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION):
    s3 = get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    # records_bytes: bytes (already NDJSON)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(records_bytes)
    buf.seek(0)
    s3.put_object(Bucket=bucket, Key=key, Body=buf.read())

def read_json_from_s3(bucket, key, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION):
    s3 = get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        body = resp["Body"].read()
        return json.loads(body)
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        if code in ("NoSuchKey", "404"):
            return None
        raise

def write_json_to_s3(bucket, key, obj, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION):
    s3 = get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(obj).encode("utf-8"))

def list_prefix(bucket, prefix):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            yield o["Key"]