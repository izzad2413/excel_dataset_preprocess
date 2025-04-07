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

# web app
def show_page():
    
    st.title("Excel Data Cleaner")
    uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)
    
    if uploaded_files:
        dfs = [pd.read_excel(file) for file in uploaded_files]
        combined_df = pd.concat(dfs, ignore_index=True)
        
        st.subheader("Original Data")
        st.dataframe(combined_df.head())
        
        cleaned_df = clean_dataset(combined_df)
        
        st.subheader("Cleaned Data")
        st.dataframe(cleaned_df.head())
        
        # Download cleaned file
        buffer = io.BytesIO()
        cleaned_df.to_excel(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
        label="Download Cleaned Excel",
        data=buffer,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    

