import streamlit as st
import pandas as pd
import io
import time

# clean the dataset
def clean_dataset(df):
    start_time = time.time()
    # remove duplicate
    df.drop_duplicates(inplace=True)
    
    # reformat data type
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount_purchase'] = df['amount_purchase'].astype(float)
    
    # replace null values
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())
            
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    
    return df, elapsed_time

# web app
def show_page():
    
    st.title("Excel Data Cleaner")
    st.markdown("""
    ### 📄 Application Description
    
    This is a simple Streamlit application designed to clean multiple datasets from Excel files. It demonstrates the basic functionality of combining and preprocessing data with a fixed structure.

    **Key features:**
    - Cleans multiple Excel files with identical column structure  
    - Supports six predefined features, combining both numerical and textual data types  
    - Handles tasks like removing duplicates, reformatting data types, and filling missing values  
    - Built for demonstration purposes only, with current limitations on flexibility and scalability  

    ⚙️ *Note: This tool is an early prototype and will be extended into a more robust and configurable data cleaning solution in future versions.*
    """)
    uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)
    
    if uploaded_files:
        dfs = [pd.read_excel(file) for file in uploaded_files]
        combined_df = pd.concat(dfs, ignore_index=True)
        
        st.subheader("Original Data")
        st.dataframe(combined_df.head())
        
        cleaned_df, processing_time = clean_dataset(combined_df)
        
        st.subheader("Cleaned Data")
        st.dataframe(cleaned_df.head())
        st.success(f"Data cleaning completed in {processing_time} seconds.")
        
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
    

