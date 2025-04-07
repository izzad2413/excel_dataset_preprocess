import streamlit as st
import pandas as pd
import io

# clean the dataset
def clean_dataset(df):
    # remove duplicate
    df.drop.duplicates(inplace=True)
    
    # reformat data type
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount_purchase'] = df['amount_purchase'].astype(float)
    
    # replace null values
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())
    
    return df