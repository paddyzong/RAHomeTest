import math
from urllib.parse import urlparse
from celery import shared_task
import pandas as pd
from io import StringIO
import boto3
from ..utils.file_utils import parse_s3_url
from ..utils.data_processing import *
from ..utils.redis_client import *
from ..utils.S3Client import S3Client

redis_client = get_redis_client()
@shared_task
def add(x, y):
    return x + y

@shared_task
def process_chunk(file_path, index, start_offset, end_offset, column_names=None, desired_types=None):
    """
    Processes a specific chunk of a file based on byte offsets.
    """
    # Check if the file path is an S3 URL
    if file_path.startswith('https'):
        # Handle S3 file
        s3_client = S3Client.get_client() 
        bucket, key = parse_s3_url(file_path)
        
        # Calculate range string for S3 GetObject
        range_str = f'bytes={start_offset}-{end_offset-1 if end_offset else ""}'
        
        response = s3_client.get_object(
            Bucket=bucket,
            Key=key,
            Range=range_str
        )
        raw_data = response['Body'].read().decode('utf-8')
    else:
        # Handle local file
        with open(file_path, 'rb') as f:
            f.seek(start_offset)
            if end_offset is None:
                raw_data = f.read().decode('utf-8')
            else:
                raw_data = f.read(end_offset - start_offset).decode('utf-8')

    # Read into a DataFrame
    df = pd.read_csv(StringIO(raw_data), header=None, names=column_names)
    df = infer_and_convert_data_types(df,desired_types)
    types = list(df.dtypes.astype(str)) 
    datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns

    for col in datetime_cols:
        df[col] = df[col].apply(format_date_based_on_precision)
    df = df.applymap(complex_to_string)
    #store_df_as_redis_hash(redis_client,file_path + ":" +str(index),df)
    store_df_as_redis_hash_batch(redis_client,file_path + ":" +str(index),df)
    return {
        "chunk_index": index,
        "start_offset": start_offset,
        "end_offset": end_offset,
        "total_records": len(df),
        "column_types": types  # Convert column types to strings
    }  # Return processed data as a dictionary

def complex_to_string(value):
    if isinstance(value, complex):
        if math.isnan(value.real) or math.isnan(value.imag):
            return ""
        return f"{value.real}+{value.imag}j" if value.imag >= 0 else f"{value.real}{value.imag}j"
    return value

def store_df_as_redis_hash(redis_client, key, df):
    #df = df.fillna("") 
    for idx, row in df.iterrows():
        hash_key = f"{key}:{idx}"
        json_data = row.to_json()
        redis_client.set(hash_key, json_data)
        redis_client.expire(hash_key, 3600)

def store_df_as_redis_hash_batch(redis_client, key, df, batch_size=100):
    total_rows = len(df)
    for start_idx in range(0, total_rows, batch_size):
        end_idx = min(start_idx + batch_size, total_rows)
        batch = df.iloc[start_idx:end_idx]  # Slice the DataFrame for the batch  
        # Use Redis pipeline for batch updates
        pipeline = redis_client.pipeline()
        
        for idx, row in batch.iterrows():
            hash_key = f"{key}:{idx}"
            json_data = row.to_json()
            pipeline.set(hash_key, json_data)
            pipeline.expire(hash_key, 3600)  # Set expiry to 1 hour
        
        pipeline.execute()  # Execute all commands in the pipeline

    print(f"Successfully stored {total_rows} rows in Redis.")
