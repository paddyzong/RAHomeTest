import pandas as pd
import numpy as np
import traceback
import time
import gc
import io

def infer_and_convert_data_types(df, desired_types=None):
    if desired_types is None:
        desired_types = {}

    for i in range(len(df.columns)):
        col = df.columns[i]  # Access column by position
        #print(col)
        if len(desired_types) > 0:
            df[col] = convert_column_to_type(df[col], desired_type=desired_types[i])
        else:
            df[col] = infer_and_convert_column(df[col])
    
    return df

non_na_ratio = 0.75
def infer_and_convert_column(column, non_na_ratio=0.75):
    not_na_mask = column.notna()
    column_no_na = column[not_na_mask]

    # Try converting to numeric (int or float)
    numeric_column = pd.to_numeric(column_no_na, errors='coerce')
    numeric_non_na_ratio = numeric_column.notnull().mean()
    if numeric_non_na_ratio >= non_na_ratio:
        # Determine if integer or float
        if np.isclose(numeric_column.dropna() % 1, 0).all():
            # All values are integers
            min_val, max_val = numeric_column.min(), numeric_column.max()
            if min_val >= np.iinfo(np.int8).min and max_val <= np.iinfo(np.int8).max:
                return pd.to_numeric(column, errors='coerce').astype('Int8')
            elif min_val >= np.iinfo(np.int16).min and max_val <= np.iinfo(np.int16).max:
                return pd.to_numeric(column, errors='coerce').astype('Int16')
            elif min_val >= np.iinfo(np.int32).min and max_val <= np.iinfo(np.int32).max:
                return pd.to_numeric(column, errors='coerce').astype('Int32')
            else:
                return pd.to_numeric(column, errors='coerce').astype('Int64')
        else:
            # Contains floats
            if numeric_column.between(np.finfo(np.float32).min, np.finfo(np.float32).max).all():
                return pd.to_numeric(column, errors='coerce').astype('float32')
            else:
                return pd.to_numeric(column, errors='coerce').astype('float64')

    # Try converting to datetime
    # Print row indices where the conversion resulted in NaT (null)
    # print(f"Processing column: {column.name}")
    # null_rows = datetime_column[datetime_column.isnull()]
    # print("Rows with null datetime values:\n", null_rows.index.tolist())
        
    # # Print row indices where the conversion was successful
    # non_null_rows = datetime_column[datetime_column.notnull()]
    # print("Rows with non-null datetime values:\n", non_null_rows.index.tolist())
    # print(datetime_non_na_ratio)
    datetime_column_dayfirst = pd.to_datetime(column_no_na, errors='coerce', dayfirst=True)
    datetime_non_na_ratio_dayfirst = datetime_column_dayfirst.notnull().mean()
    
    # Fallback: Attempt conversion with dayfirst=False if the first attempt failed
    datetime_column_monthfirst = pd.to_datetime(column_no_na, errors='coerce', dayfirst=False)
    datetime_non_na_ratio_monthfirst = datetime_column_monthfirst.notnull().mean()
    
    if datetime_non_na_ratio_dayfirst >= non_na_ratio and datetime_non_na_ratio_monthfirst >= non_na_ratio:
    # Both exceed non_na_ratio; choose the one with the higher ratio
        if datetime_non_na_ratio_dayfirst >= datetime_non_na_ratio_monthfirst:
            return pd.to_datetime(column, errors='coerce', dayfirst=True)
        else:
            return pd.to_datetime(column, errors='coerce', dayfirst=False)
    elif datetime_non_na_ratio_dayfirst >= non_na_ratio:
        # Only dayfirst=True meets the threshold
        return pd.to_datetime(column, errors='coerce', dayfirst=True)
    elif datetime_non_na_ratio_monthfirst >= non_na_ratio:
        # Only dayfirst=False meets the threshold
        return pd.to_datetime(column, errors='coerce', dayfirst=False)

    # Try converting to timedelta
    timedelta_column = pd.to_timedelta(column_no_na, errors='coerce')
    timedelta_non_na_ratio = timedelta_column.notnull().mean()
    if timedelta_non_na_ratio >= non_na_ratio:
        return pd.to_timedelta(column, errors='coerce')

    # Try converting to complex numbers using a helper function
    def safe_complex(x):
        try:
            return complex(x)
        except ValueError:
            return np.nan

    complex_column = column_no_na.apply(lambda x: safe_complex(x) if pd.notnull(x) else np.nan)
    complex_non_na_ratio = complex_column.notnull().mean()
    if complex_non_na_ratio >= non_na_ratio:
        return complex_column.astype('complex128')

    # Try to identify boolean values
    bool_values = {
        'true': True, 'false': False,
        'yes': True, 'no': False,
        '1': True, '0': False,
        't': True, 'f': False,
        'y': True, 'n': False,
        True: True, False: False
    }
    lower_column = column_no_na.astype(str).str.strip().str.lower()
    is_bool = lower_column.isin(bool_values.keys())
    bool_non_na_ratio = is_bool.mean()
    if bool_non_na_ratio >= non_na_ratio:
        converted_column = column.astype(str).str.strip().str.lower().map(bool_values).astype('boolean')
        return converted_column

    # Check for categorical data
    unique_ratio = column_no_na.nunique() / len(column_no_na)
    if unique_ratio <= 0.4:
        return column.astype('category')

    # Return original column if no conversion applies
    return column
    
def convert_column_to_type(column, desired_type):
    # Define inverse mapping from desired types to pandas data types
    inverse_data_type_mapping = {
        'Text': ['string', 'object'],
        'Integer': ['Int64', 'Int32', 'Int16', 'Int8'],
        'Decimal': ['float64', 'float32'],
        'Boolean': ['boolean', 'bool'],
        'Date': ['datetime64[ns]'],
        'Duration': ['timedelta64[ns]'],
        'Category': ['category'],
        'Complex': ['complex128']
    }

    try:
        if desired_type not in inverse_data_type_mapping:
            raise ValueError(f"Unsupported desired_type: {desired_type}")

        if desired_type == 'Text':
            # Convert to string type
            return column.astype('string')

        elif desired_type == 'Integer':
            # Convert column to numeric, coercing errors to NaN
            numeric_column = pd.to_numeric(column, errors='coerce')
            if numeric_column.notnull().any():
                # Determine the smallest integer type that fits the data
                min_val, max_val = numeric_column.min(), numeric_column.max()
                if min_val >= np.iinfo(np.int8).min and max_val <= np.iinfo(np.int8).max:
                    return pd.to_numeric(column, errors='coerce').astype('Int8')
                elif min_val >= np.iinfo(np.int16).min and max_val <= np.iinfo(np.int16).max:
                    return pd.to_numeric(column, errors='coerce').astype('Int16')
                elif min_val >= np.iinfo(np.int32).min and max_val <= np.iinfo(np.int32).max:
                    return pd.to_numeric(column, errors='coerce').astype('Int32')
                else:
                    return pd.to_numeric(column, errors='coerce').astype('Int64')
            else:
                # If all values are NaN after conversion, cannot convert to Integer
                print("Warning: Cannot convert column to Integer type; all values are non-numeric or missing.")
                return column

        elif desired_type == 'Decimal':
            # Convert to float64
            numeric_column = pd.to_numeric(column, errors='coerce')
            # Convert to float64
            if numeric_column.between(np.finfo(np.float32).min, np.finfo(np.float32).max).all():
                return pd.to_numeric(column, errors='coerce').astype('float32')
            else:
                return pd.to_numeric(column, errors='coerce').astype('float64')

        elif desired_type == 'Boolean':
            # Map common boolean representations
            bool_values = {
                'true': True, 'false': False,
                'yes': True, 'no': False,
                '1': True, '0': False,
                't': True, 'f': False,
                'y': True, 'n': False,
                True: True, False: False
            }
            # Convert to lowercase strings for mapping
            lower_column = column.astype(str).str.strip().str.lower()
            converted_column = lower_column.map(bool_values)
            # Any value not in bool_values will be NaN
            return converted_column.astype('boolean')

        elif desired_type == 'Date':
            # Convert to datetime64[ns]
            # Convert with dayfirst=True
            datefirst = pd.to_datetime(column, errors='coerce', dayfirst=True)
            non_na_ratio_datefirst = datefirst.notnull().mean()

            # Convert with dayfirst=False
            monthfirst = pd.to_datetime(column, errors='coerce', dayfirst=False)
            non_na_ratio_monthfirst = monthfirst.notnull().mean()

            # Compare the non-null ratios and return the conversion with the higher ratio
            if non_na_ratio_datefirst >= non_na_ratio_monthfirst:
                return datefirst
            else:
                return monthfirst

        elif desired_type == 'Duration':
            # Convert to timedelta64[ns]
            return pd.to_timedelta(column, errors='coerce')

        elif desired_type == 'Category':
            # Convert to category
            return column.astype('category')

        elif desired_type == 'Complex':
            # Convert to complex128 using a helper function
            def safe_complex(x):
                try:
                    return complex(x)
                except ValueError:
                    return np.nan
            converted_column = column.apply(lambda x: safe_complex(x) if pd.notnull(x) else np.nan)
            return converted_column.astype('complex128')

        else:
            raise ValueError(f"Conversion for desired_type '{desired_type}' is not implemented.")

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
        print(f"Error converting column to {desired_type}: {e}")
        return column  # Return the original column if conversion fails


def format_date_based_on_precision(dt):
    if pd.isnull(dt):
        return None  # Handle missing (NaN) dates
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt.strftime("%Y-%m-%d")  # Only date part if there's no time information
    elif dt.microsecond == 0:
        return dt.strftime("%Y-%m-%d %H:%M")  # Date and hour:minute if no microseconds
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")  # Full datetime with microseconds

import pandas as pd
from concurrent.futures import ProcessPoolExecutor

# Process function for a chunk
def load_and_process_csv_in_chunks(file_path, chunksize=50000, desired_types=None, non_na_ratio=0.75):
    chunk_results = []

    # Process each chunk in parallel
    with ProcessPoolExecutor() as executor:
        # Read file in chunks
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            # Submit each chunk to the executor
            future = executor.submit(infer_and_convert_data_types, chunk)
            chunk_results.append(future)

    # Combine all processed chunks
    processed_chunks = [future.result() for future in chunk_results]
    df_combined = pd.concat(processed_chunks, ignore_index=True)

    return df_combined

def load_and_process_csv_in_chunks_serial(file_path, chunksize=50000, desired_types=None, non_na_ratio=0.75):
    processed_chunks = []

    # Read file in chunks and process each chunk serially
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        # Process the chunk directly without parallelism
        processed_chunk = infer_and_convert_data_types(chunk, desired_types=desired_types)
        processed_chunks.append(processed_chunk)

    # Combine all processed chunks
    df_combined = pd.concat(processed_chunks, ignore_index=True)

    return df_combined

def load_and_process(file_path):
    # Read file in chunks and process each chunk serially
    df = pd.read_csv(file_path)
    df_processed = infer_and_convert_data_types(df)

    return df_processed
def capture_info(df, name):
    """Capture the .info() output of a DataFrame and return it as a string."""
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    buffer.close()
    return info_str

# Example usage
if __name__ == '__main__':
   #file_path = 'generated_data_1GB.csv'  
    file_path = 'err.csv'
    #file_path = 'generated_data.csv' 

    df_info_outputs = {}

    start_time_serial = time.time()
    df_serial = load_and_process(file_path)
    df_info_outputs['df_serial'] = capture_info(df_serial, 'df_serial')
    end_time_serial = time.time()
    duration_serial = end_time_serial - start_time_serial
    del df_serial
    gc.collect()

    start_time_serial_with_chunk = time.time()
    df_serial_with_chunk = load_and_process_csv_in_chunks_serial(file_path)
    df_info_outputs['df_serial_with_chunk'] = capture_info(df_serial_with_chunk, 'df_serial_with_chunk')
    end_time_serial_with_chunk = time.time()
    duration_serial_with_chunk = end_time_serial_with_chunk - start_time_serial_with_chunk
    del df_serial_with_chunk
    gc.collect()

    start_time_parallel = time.time()
    df_combined = load_and_process_csv_in_chunks(file_path)
    df_info_outputs['df_combined'] = capture_info(df_combined, 'df_combined')
    end_time_parallel = time.time()
    duration_parallel = end_time_parallel - start_time_parallel
    del df_combined
    gc.collect()

    for df_name, info_str in df_info_outputs.items():
        print(f"--- {df_name} info ---\n{info_str}\n")

    print(f"Parallel processing time: {duration_parallel:.2f} seconds\n")
    print(f"Serial processing time: {duration_serial:.2f} seconds\n")
    print(f"Serial with chunk processing time: {duration_serial_with_chunk:.2f} seconds\n")