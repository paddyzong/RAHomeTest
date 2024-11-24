from celery import group
from collections import Counter
from ..utils.data_processing import *
from .tasks import *
from collections import defaultdict
from ..utils.redis_client import *

redis_client = get_redis_client()
def calculate_byte_offsets(file_path, chunksize):
    byte_offsets = []  # Start at the beginning of the file
    with open(file_path, 'rb') as f:
        lines_read = 0
        s = f.readline()
        print(s)
        byte_offsets.append(f.tell()) #offset of header
        while True:
            line = f.readline()
            if not line:
                break
            lines_read += 1
            if lines_read % chunksize == 0:
                byte_offsets.append(f.tell())  # Get byte offset of the next line
        f.seek(0, 2)  # Seek to the end of the file
        end_offset = f.tell()  # Get the offset
        print("end offset:"+str(end_offset))
    if byte_offsets[-1] != end_offset:
        byte_offsets.append(end_offset)  # End of file marker
    redis_client.set(f"{file_path}:total_records", lines_read)
    redis_client.expire(f"{file_path}:total_records", 3600)
    redis_client.set(f"{file_path}:chunksize", chunksize)
    redis_client.expire(f"{file_path}:chunksize", 3600)
    redis_client.set(f"{file_path}:total_chunks", len(byte_offsets)-1)
    redis_client.expire(f"{file_path}:total_chunks", 3600)
    return byte_offsets

import json
def submit_chunks_to_workers(file_path, chunksize, column_names=None, desired_types=None):
    # Calculate byte offsets
    byte_offsets = calculate_byte_offsets(file_path, chunksize)
    print(byte_offsets)
    json_data = json.dumps(byte_offsets)
    key = file_path + ":offsets"
    redis_client.set(key, json_data)
    redis_client.expire(key, 3600) 
    # Create tasks for each chunk
    tasks = []
    for i in range(len(byte_offsets) - 1):
        start_offset = byte_offsets[i]
        end_offset = byte_offsets[i + 1]
        tasks.append(process_chunk.s(file_path, i, start_offset, end_offset, column_names,desired_types)) 

    # Submit tasks as a group
    task_group = group(tasks)
    async_result = task_group.apply_async()
    results = async_result.get()
    column_type_counts = defaultdict(lambda: defaultdict(int))

    # Process each result
    for result in results:
        for col_index, col_type in enumerate(result["column_types"]):
            column_type_counts[col_index][col_type] += 1

    # Convert to a normal dictionary for better visualization
    column_type_counts = {col: dict(type_counts) for col, type_counts in column_type_counts.items()}
    print(column_type_counts)
    most_frequent_types_with_counts = {
    col: (max(type_counts, key=type_counts.get), max(type_counts.values()))
    for col, type_counts in column_type_counts.items()
    }
    most_frequent_types = [
    max(type_counts, key=type_counts.get)
    for col, type_counts in column_type_counts.items()
    ]
    from ..views import data_type_mapping
    converted_types = [data_type_mapping.get(data_type, "Unknown") for data_type in most_frequent_types]
    
    json_data = json.dumps(converted_types)
    key = file_path + ":types"
    redis_client.set(key, json_data)
    redis_client.expire(key, 3600)  

    for col, (most_frequent_type, count) in most_frequent_types_with_counts.items():
        print(f"Column {col}: Most frequent type is '{most_frequent_type}' with count {count}")
    tasks = []
    for result_index,result in enumerate(results):
        should_continue_outer = False  # Flag to skip to the next iteration of the outer loop
        for col_index, col_type in enumerate(result["column_types"]):
            if(col_type!=most_frequent_types[col_index]):
                start_offset = byte_offsets[result_index]
                end_offset = byte_offsets[result_index + 1]
                tasks.append(process_chunk.s(file_path, result_index, start_offset, end_offset, column_names,converted_types))
                should_continue_outer = True  # Set the flag
                break  # Exit the inner loop

        if should_continue_outer:
            continue  # Skip to the next iteration of the outer loop
    task_group = group(tasks)
    async_result = task_group.apply_async()
    results = async_result.get()
    return most_frequent_types_with_counts

def get_column_names(file_path):
    """
    Reads the first line of the file to extract column names.
    """
    with open(file_path, 'r') as f:
        header_line = f.readline().strip()  # Read the first line and remove extra whitespace
    column_names = header_line.split(',')  # Split by delimiter (default: comma)
    return column_names
