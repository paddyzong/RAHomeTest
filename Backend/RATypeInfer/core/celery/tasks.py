from celery import shared_task
import pandas as pd
from io import StringIO
import redis
from ..utils.data_processing import *

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@shared_task
def add(x, y):
    return x + y

@shared_task
def process_chunk(file_path, index, start_offset, end_offset, column_names=None):
    """
    Processes a specific chunk of a file based on byte offsets.
    """
    print(11111111111)
    print(file_path)
    with open(file_path, 'rb') as f:
        f.seek(start_offset)
        if end_offset is None:
            raw_data = f.read().decode('utf-8')  # Read until the end of the file
        else:
            raw_data = f.read(end_offset - start_offset).decode('utf-8')  # Read the specified range

        
    # Remove partial rows if not at the start
    if start_offset != 0:
        raw_data = raw_data[raw_data.find('\n') + 1:]
    
    # Read into a DataFrame
    df = pd.read_csv(StringIO(raw_data), header=None, names=column_names)
    df = infer_and_convert_data_types(df)
    # Perform some processing (modify as needed)
    store_df_as_redis_hash(redis_client,file_path,df)
    return {
        "chunk_index": index,
        "start_offset": start_offset,
        "end_offset": end_offset,
        "column_types": list(df.dtypes.astype(str))  # Convert column types to strings
    }  # Return processed data as a dictionary

def store_df_as_redis_hash(redis_client, key, df):
    #df = df.fillna("") 
    for idx, row in df.iterrows():
        json_data = row.to_json()
        redis_client.set(f"{key}:{idx}", json_data)