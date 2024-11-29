from celery import group
from collections import Counter
from ..utils.data_processing import *
from .tasks import *
from collections import defaultdict
from ..utils.redis_client import *

redis_client = get_redis_client()
def calculate_byte_offsets(file_path, chunksize):
    byte_offsets = []  # Initialize byte offsets
    with open(file_path, 'rb') as f:
        # Read and handle the header
        header = f.readline()  # Read the header line
        print(header)  # Optional: Display the header for debugging
        byte_offsets.append(f.tell())  # Offset after the header

        # Calculate chunk offsets
        file_size = f.seek(0, 2)  # Get the total file size
        for offset in range(chunksize, file_size, chunksize):
            f.seek(offset)  # Move to the chunk boundary
            f.readline()  # Adjust to the next newline
            byte_offsets.append(f.tell())  # Record the adjusted offset
        
        byte_offsets.append(file_size)  # Add the end of file marker
        
    redis_client.set(f"{file_path}:total_chunks", len(byte_offsets)-1)
    redis_client.expire(f"{file_path}:total_chunks", 3600)
    return byte_offsets

import json
def submit_chunks_to_workers(file_path, chunksize, column_names=None, desired_types=None):
    # Calculate byte offsets
    byte_offsets = calculate_byte_offsets(file_path, chunksize)

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
    total_records = 0
    index_ranges = []
    current_index = 0

    for result in results:
        total_records += result["total_records"]
        
        start_index = current_index
        end_index = current_index + result["total_records"] - 1
        index_ranges.append((start_index, end_index))
        
        current_index = end_index + 1
        
        for col_index, col_type in enumerate(result["column_types"]):
            column_type_counts[col_index][col_type] += 1

    redis_client.set(f"{file_path}:index_ranges", json.dumps(index_ranges))

    # Optionally, store total_records_sum as well
    redis_client.set(f"{file_path}:total_records", total_records)

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
