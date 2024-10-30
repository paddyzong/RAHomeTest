# my_app/utils/file_utils.py

import pandas as pd
from django.core.exceptions import ValidationError

def is_csv_file_empty(file_path):
    """Check if a CSV file is empty by reading the first row."""
    try:
        data = pd.read_csv(file_path, nrows=1)
        return data.empty
    except pd.errors.EmptyDataError:
        return True
    except Exception as e:
        raise ValidationError(f"Error reading CSV file: {e}")

def is_excel_file_empty(file_path):
    """Check if all sheets in an Excel file are empty by only reading the first row of each sheet."""
    try:
        # Load only the first row of each sheet
        excel_data = pd.read_excel(file_path, sheet_name=None, nrows=1)
        
        # Check if all sheets are empty (no rows or columns)
        return all(df.empty or df.shape[0] == 0 for df in excel_data.values())
    
    except Exception as e:
        raise ValidationError(f"Error reading Excel file: {e}")
