import os
import pandas as pd
import random
from faker import Faker
import numpy as np

# Initialize
fake = Faker()
num_files = 10 # files generated
rows_per_file = 1000  # generate number of samples
save_dir = '../../../data/raw'

# Ensure directory exists
os.makedirs(save_dir, exist_ok=True)

# Column options
items = ['product_1', 'product_2', 'product_3']
statuses = ['yes', 'no']
feedbacks = ['worse', 'bad', 'neutral', 'good', 'great']
date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d %b %Y']

# Function to introduce random NaN values in a column
def introduce_missing_values(column_data, missing_percentage=0.1):
    # missing_percentage: Chance of each value being set to NaN
    return [np.nan if random.random() < missing_percentage else val for val in column_data]

# Dataset generation loop
for file_num in range(1, num_files + 1):
    unique_ids = random.sample(range(100000, 999999), rows_per_file)
    data = []

    for i in range(rows_per_file):
        row = {
            'id': unique_ids[i],
            'item': random.choice(items),
            'status': random.choice(statuses),
            'feedback': random.choice(feedbacks),
            'date': fake.date(pattern=random.choice(date_formats)),
            'amount_purchase': round(random.uniform(0, 1000), 2)
        }
        data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Introduce NaN values randomly for each column except 'id'
    df['item'] = introduce_missing_values(df['item'])
    df['status'] = introduce_missing_values(df['status'])
    df['feedback'] = introduce_missing_values(df['feedback'])
    df['date'] = introduce_missing_values(df['date'])
    df['amount_purchase'] = introduce_missing_values(df['amount_purchase'], missing_percentage=0.2)  # More chance for missing in 'amount_purchase'

    # File path and save
    file_path = os.path.join(save_dir, f'dataset_{file_num}.xlsx')
    df.to_excel(file_path, index=False)

    print(f'✅ Saved: {file_path}')

print("🎉 All datasets with missing values generated successfully!")