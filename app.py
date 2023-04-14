pip install -r requirements.txt
import streamlit as st
import pandas as pd
from preprocess import preprocess_data
import base64
from PIL import Image
import openpyxl

# Set the app title and logo
st.title("INSOFE Faculty Report Application")

# File uploader widget
file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if file is not None:
    file_extension = file.name.split(".")[-1]
    
    # Load the dataset into a Pandas DataFrame
    if file_extension == "csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, engine='openpyxl')
    
    # Preprocess the dataset using the preprocess_data() function
    df_processed = preprocess_data(df)
    
    # Display the processed dataset in the app
    st.write(df_processed)
    
    # Add a button to download the processed dataset as Excel
    excel = df_processed.to_excel("processed_data.xlsx", index=True, engine='openpyxl')
    with open("processed_data.xlsx", "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="processed_data.xlsx">Download processed data</a>'
        st.markdown(href, unsafe_allow_html=True)
