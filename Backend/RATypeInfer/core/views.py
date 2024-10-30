from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
import os
import traceback
from rest_framework.exceptions import ValidationError
from .utils.file_utils import *
from .utils.data_processing import *

# Create your views here.
def process(request):
    data = json.loads(request.body)  # Parse JSON data
    fileUrl = data.get('fileUrl', None)
    if fileUrl == None:
        raise ValidationError("File URL is required.")
    types = []
    specify_types_manually = data.get('specifyTypesManually', False)
    if(specify_types_manually):
        types = data.get('types', None)

    file_path = os.path.join(settings.MEDIA_ROOT,fileUrl) 
    file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension in lowercase

    try:
        # Check the file extension and read the file accordingly
        if file_extension == ".csv":
            if is_csv_file_empty(file_path):
               return JsonResponse(
                {"error": "The file is empty."},
                status=status.HTTP_400_BAD_REQUEST
            ) 
            df = pd.read_csv(file_path)
        elif file_extension in [".xls", ".xlsx"]:
            if is_excel_file_empty(file_path):
               return JsonResponse(
                {"error": "The file is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )  
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

