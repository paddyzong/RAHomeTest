import pandas as pd
import random
from faker import Faker

def generate_random_csv(num_rows, file_path='random_data.csv'):
    fake = Faker()
    data = {
        "Name": [fake.first_name() for _ in range(num_rows)],
        "Birthdate": [fake.date_of_birth(minimum_age=20, maximum_age=60).strftime("%d/%m/%Y") for _ in range(num_rows)],
        "Score": [
            str(random.choices(
                [random.randint(50, 100), "Not Available"], 
                weights=[0.8, 0.2]  # 80% for numbers, 20% for "Not Available"
            )[0]) for _ in range(num_rows)
        ],
        "Grade": [random.choice(["A", "B", "C", "D"]) for _ in range(num_rows)]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Random data saved to {file_path}")

# Example usage:
generate_random_csv(100000, "generated_data.csv")
