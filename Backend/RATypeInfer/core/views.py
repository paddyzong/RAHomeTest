from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import numpy as np
import json
import os
import traceback
# Create your views here.
def process(request):
    data = json.loads(request.body)  # Parse JSON data
    fileUrl = data.get('fileUrl', None)
    types = []
    specify_types_manually = data.get('specifyTypesManually', False)
    if(specify_types_manually):
        types = data.get('types', None)

    file_path = os.path.join(settings.MEDIA_ROOT,fileUrl) 
    file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension in lowercase

    try:
        # Check the file extension and read the file accordingly
        if file_extension == ".csv":
            df = pd.read_csv(file_path)
        elif file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
        else:
            return JsonResponse(
                {"error": "Unsupported file type. Please upload a CSV or Excel file."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    except pd.errors.EmptyDataError:
        traceback.print_exc()  # Print the full error stack trace
        return JsonResponse(
            {"error": "The file is empty."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except pd.errors.ParserError:
        traceback.print_exc()  # Print the full error stack trace
        return JsonResponse(
            {"error": "The file could not be parsed correctly. Please check the file format."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        traceback.print_exc()  # Print the full error stack trace
        return JsonResponse(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    print("Data types before inference:")
    print(df.dtypes)

    df = infer_and_convert_data_types(df,types)
    print("\nData types after inference:")
    print(df.dtypes)
    df_copy = df.copy()
    df_copy = df_copy.replace({np.nan: None})
    datetime_cols = df_copy.select_dtypes(include=['datetime64[ns]']).columns

    # Apply formatting function only to datetime columns
    for col in datetime_cols:
        df_copy[col] = df_copy[col].apply(format_date_based_on_precision)

    #    Convert the modified DataFrame to JSON
    json_data = df_copy.to_dict(orient="records")
    #print(json_data)
    data_type_mapping = {
        'object': 'Text',
        'string': 'Text',
        'int8': 'Integer',
        'Int8': 'Integer',
        'int16': 'Integer',
        'Int16': 'Integer',
        'int32': 'Integer',
        'Int32': 'Integer',
        'int64': 'Integer',
        'Int64': 'Integer',
        'float32': 'Decimal',
        'float64': 'Decimal',
        'bool': 'Boolean',
        'boolean': 'Boolean',
        'datetime64[ns]': 'Date',
        'timedelta64[ns]': 'Duration',
        'category': 'Category',
        'complex': 'Complex',
        'complex128': 'Complex'
    }

    column_types = [data_type_mapping.get(dtype, "Unknown") for dtype in df.dtypes.astype(str)]
    # Return JSON response
    return JsonResponse({"data":json_data,"types":column_types}, safe=False)

def upload(request):
        file = request.FILES["file"]

        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the file to MEDIA_ROOT
            file_path = os.path.join('uploads', file.name)  # Subdirectory 'uploads' inside MEDIA_ROOT
            path = default_storage.save(file_path, ContentFile(file.read()))

            return JsonResponse({
                "message": "File uploaded successfully",
                "file_url": path,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    datetime_column = pd.to_datetime(column_no_na, errors='coerce')
    datetime_non_na_ratio = datetime_column.notnull().mean()
    if datetime_non_na_ratio >= non_na_ratio:
        return pd.to_datetime(column, errors='coerce')

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
            return pd.to_datetime(column, errors='coerce')

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
