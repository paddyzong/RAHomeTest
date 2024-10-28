from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
import os
# Create your views here.
def process(request):
    data = json.loads(request.body)  # Parse JSON data
    fileUrl = data.get('fileUrl', None)
    types = data.get('types', None)
    file_path = os.path.join(settings.MEDIA_ROOT,fileUrl) 
    print(file_path)
    df = pd.read_csv(file_path)
    print("Data types before inference:")
    print(df.dtypes)

    df = infer_and_convert_data_types(df)

    print("\nData types after inference:")
    print(df.dtypes)
    df_copy = df.copy()
    datetime_cols = df_copy.select_dtypes(include=['datetime64[ns]']).columns

    # Apply formatting function only to datetime columns
    for col in datetime_cols:
        df_copy[col] = df_copy[col].apply(format_date_based_on_precision)

    #    Convert the modified DataFrame to JSON
    json_data = df_copy.to_dict(orient="records")
    #print(json_data)
    data_type_mapping = {
    'object': 'Text',
    'int64': 'Integer',
    'float64': 'Decimal',
    'bool': 'Boolean',
    'datetime64[ns]': 'Date',
    'timedelta[ns]': 'Duration',
    'category': 'Category'
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

def infer_and_convert_data_types(df):
    for col in df.columns:
        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])

    return df

def format_date_based_on_precision(dt):
    if pd.isnull(dt):
        return None  # Handle missing (NaN) dates
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt.strftime("%Y-%m-%d")  # Only date part if there's no time information
    elif dt.microsecond == 0:
        return dt.strftime("%Y-%m-%d %H:%M")  # Date and hour:minute if no microseconds
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")  # Full datetime with microseconds
