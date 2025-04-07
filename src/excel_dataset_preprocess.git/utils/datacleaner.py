import pandas as pd
import glob
import os

def clean_excel_files(folder_path, output_file):
    # Read all Excel files
    files = glob.glob(os.path.join(folder_path, '*.xlsx'))
    if not files:
        print("No Excel files found.")
        return

    df_list = [pd.read_excel(file) for file in files]
    df = pd.concat(df_list, ignore_index=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Reformat columns
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Date
    df['amount_purchase'] = df['amount_purchase'].astype(float)  # Currency

    # Fill nulls
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    # Save cleaned file
    df.to_excel(output_file, index=False)
    print(f"✅ Cleaned data saved to {output_file}")
