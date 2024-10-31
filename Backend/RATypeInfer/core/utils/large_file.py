import pandas as pd
import random
from faker import Faker
import csv

def generate_random_csv(num_rows, file_path='random_data.csv', chunk_size=100000):
    fake = Faker()
    
    # Predefine a smaller pool of names to speed up random choice
    names_pool = [fake.first_name() for _ in range(1000)]
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Birthdate", "Score", "Grade"])  # Write headers
        
        for _ in range(0, num_rows, chunk_size):
            # Generate a chunk of data
            chunk_data = [
                [
                    random.choice(names_pool),
                    fake.date_of_birth(minimum_age=20, maximum_age=60).strftime("%d/%m/%Y"),
                    str(random.choices(
                        [random.randint(50, 100), "Not Available"], 
                        weights=[0.8, 0.2]
                    )[0]),
                    random.choice(["A", "B", "C", "D"])
                ]
                for _ in range(chunk_size)
            ]
            
            # Write the chunk to CSV
            writer.writerows(chunk_data)
            print(f"Written {chunk_size} rows to {file_path}")

    print(f"Random data saved to {file_path}")

# Generate approximately 1GB of data
generate_random_csv(10000000, "generated_data_1GB.csv")  # Adjust row count if needed
