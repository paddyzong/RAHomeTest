from celery import group
from collections import Counter
from ..utils.data_processing import *
from .tasks import *

def calculate_byte_offsets(file_path, chunksize):
    byte_offsets = [0]  # Start at the beginning of the file
    with open(file_path, 'rb') as f:
        lines_read = 0
        while True:
            line = f.readline()
            if not line:
                break
            lines_read += 1
            if lines_read % chunksize == 0:
                byte_offsets.append(f.tell())  # Get byte offset of the next line
    byte_offsets.append(None)  # End of file marker
    return byte_offsets

def submit_chunks_to_workers(file_path, chunksize, column_names=None):
    # Calculate byte offsets
    byte_offsets = calculate_byte_offsets(file_path, chunksize)
    print(byte_offsets)
    
    # Create tasks for each chunk
    tasks = []
    for i in range(len(byte_offsets) - 1):
        start_offset = byte_offsets[i]
        end_offset = byte_offsets[i + 1]
        print(str(start_offset)+","+str(end_offset))
        tasks.append(process_chunk.s(file_path, i, start_offset, end_offset, column_names))
    
    # Submit tasks as a group
    task_group = group(tasks)
    async_result = task_group.apply_async()
    results = async_result.get()
    type_counter = Counter()

    for result in results:
        type_counter.update(result["column_types"])

    print("Data Type Counts:")
    for data_type, count in type_counter.items():
        print(f"{data_type}: {count}")
    
    return async_result

def get_column_names(file_path):
    """
    Reads the first line of the file to extract column names.
    """
    with open(file_path, 'r') as f:
        header_line = f.readline().strip()  # Read the first line and remove extra whitespace
    column_names = header_line.split(',')  # Split by delimiter (default: comma)
    return column_names

def store_df_as_redis_hash(redis_client, key, df):
    for idx, row in df.iterrows():
        redis_client.hset(f"{key}:{idx}", mapping=row.to_dict())

def main():
    # Specify file path and chunk size
    file_path = "/Users/haopengzong/Home Test/RAHomeTest/sample_data/sample_data.csv"  # Update with your actual file path
    chunksize = 50000  # Number of rows per chunk

    column_names = get_column_names(file_path)

    # Submit tasks to workers and retrieve results
    print("Submitting tasks to Celery workers...")
    async_result = submit_chunks_to_workers(file_path, chunksize,column_names)

    # Wait for results and print data type counts
    if async_result.ready():
        print("All tasks completed successfully!")
        print("Results processed.")
    else:
        print("Tasks are still running. Please check back later.")

if __name__ == "__main__":
    main()