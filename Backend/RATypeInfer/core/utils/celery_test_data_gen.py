import pandas as pd
import random
from faker import Faker

def generate_synthetic_data(num_rows):
    """
    Generate a synthetic dataset with a specified number of rows.
    
    Parameters:
        num_rows (int): Number of rows to generate.
    
    Returns:
        pd.DataFrame: Synthetic dataset.
    """
    # Initialize Faker for generating random names and dates
    fake = Faker()

    # Generate synthetic data
    data = {
        "Name": [fake.first_name() for _ in range(num_rows)],
        "Birthdate": [fake.date_of_birth(minimum_age=20, maximum_age=60).strftime('%d/%m/%Y') for _ in range(num_rows)],
        "Score": [random.choice([random.randint(60, 100), "Not Available"]) for _ in range(num_rows)],
        "Grade": [
            random.choice(['A', 'B', 'C']) if i < num_rows / 2 else random.randint(1, 100)
            for i in range(num_rows)
        ]
    }

    # Create and return a DataFrame
    return pd.DataFrame(data)

# Example Usage
num_rows = 200  # Set the number of rows here
synthetic_data = generate_synthetic_data(num_rows)

# Save to CSV
synthetic_data.to_csv('/Users/haopengzong/Home Test/RAHomeTest/sample_data/celery_sample_data.csv', index=False)

print(f"Synthetic dataset with {num_rows} rows saved as 'celery_sample_data.csv'.")
