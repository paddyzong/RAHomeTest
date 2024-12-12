import unittest
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from ..utils.data_processing import *

class TestDataTypeInferenceAndConversion(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        # Create a test CSV file
        cls.test_csv_path = "test_data.csv"
        # Define test data
        df = pd.DataFrame({
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'dates': pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03', None, '2020-01-05']),
            'strings': ['apple', 'banana', 'cherry', 'date', 'elderberry']
        })
        
        df.to_csv(cls.test_csv_path, index=False)
        cls.data_type_test_csv_path = "data_type_test_data.csv"
        
        #Create a DataFrame with each column representing a different data type
        df = pd.DataFrame({
            'numeric': [1.1, 2.2, np.nan, 4.4, 5.5],
            'integer': [1, 2, 3, np.nan, 5],
            'datetime': ['2020-01-01', '2020-02-01', None, '2020-03-01', '2020-04-01'],
            'boolean': ['yes', 'no', 'yes', 'no', 'yes'],
            'complex': ['1+2j', '3+4j', '5+6j', None, '7+8j'],
            'categorical': ['apple', 'banana', 'apple', 'banana', 'apple']
        })
        
        #Save the DataFrame to a CSV file
        df.to_csv(cls.data_type_test_csv_path, index=False)

 
    @classmethod
    def tearDownClass(cls):
        # Remove the test CSV file after tests complete
        if os.path.exists(cls.test_csv_path):
            os.remove(cls.test_csv_path)
        
        if os.path.exists(cls.data_type_test_csv_path):
            os.remove(cls.data_type_test_csv_path)

    def test_infer_and_convert_data_types(self):
        # Test data
        df = pd.read_csv(self.test_csv_path)

        # Expected output types without explicit desired types
        inferred_df = infer_and_convert_data_types(df)
        self.assertTrue(pd.api.types.is_integer_dtype(inferred_df['integers']))
        self.assertTrue(pd.api.types.is_float_dtype(inferred_df['floats']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(inferred_df['dates']))
        self.assertTrue(pd.api.types.is_string_dtype(inferred_df['strings']))

    def test_infer_and_convert_column_from_csv(self):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.data_type_test_csv_path)

        # Test numeric column
        converted_column = infer_and_convert_column(df['numeric'])
        self.assertTrue(pd.api.types.is_float_dtype(converted_column), 
                        "Expected float type for numeric column")

        # Test integer column
        converted_column = infer_and_convert_column(df['integer'])
        self.assertTrue(pd.api.types.is_integer_dtype(converted_column), 
                        "Expected integer type for integer column")

        # Test datetime column
        converted_column = infer_and_convert_column(df['datetime'])
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(converted_column), 
                        "Expected datetime type for datetime column")

        # Test boolean column
        converted_column = infer_and_convert_column(df['boolean'])
        self.assertTrue(pd.api.types.is_bool_dtype(converted_column), 
                        "Expected boolean type for boolean column")

        # Test complex column
        converted_column = infer_and_convert_column(df['complex'])
        self.assertTrue(pd.api.types.is_complex_dtype(converted_column), 
                        "Expected complex type for complex column")

        # Test categorical column
        converted_column = infer_and_convert_column(df['categorical'])
        self.assertTrue(pd.api.types.is_categorical_dtype(converted_column), 
                        "Expected categorical type for categorical column")

    def test_convert_column_to_type_from_csv(self):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.data_type_test_csv_path)

        # Test desired conversion to 'Integer'
        converted_column = convert_column_to_type(df['integer'], 'Integer')
        self.assertTrue(pd.api.types.is_integer_dtype(converted_column), 
                        "Expected integer type for Integer conversion")

        # Test desired conversion to 'Decimal'
        converted_column = convert_column_to_type(df['numeric'], 'Decimal')
        self.assertTrue(pd.api.types.is_float_dtype(converted_column), 
                        "Expected float type for Decimal conversion")

        # Test desired conversion to 'Date'
        converted_column = convert_column_to_type(df['datetime'], 'Date')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(converted_column), 
                        "Expected datetime type for Date conversion")

        # Test desired conversion to 'Boolean'
        converted_column = convert_column_to_type(df['boolean'], 'Boolean')
        self.assertTrue(pd.api.types.is_bool_dtype(converted_column), 
                        "Expected boolean type for Boolean conversion")

        # Test desired conversion to 'Complex'
        converted_column = convert_column_to_type(df['complex'], 'Complex')
        self.assertTrue(pd.api.types.is_complex_dtype(converted_column), 
                        "Expected complex type for Complex conversion")

if __name__ == '__main__':
    unittest.main()