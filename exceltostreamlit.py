import streamlit as st
import pandas as pd
from pandasql import sqldf  # Allows SQL-like queries on pandas DataFrames

# Function to execute SQL queries
def run_query(query, data):
    try:
        return sqldf(query, locals())  # Run the SQL query on the DataFrame
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("Excel to Queryable Database")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read the Excel file into a DataFrame
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Preview of your data:")
        st.dataframe(df)  # Display the DataFrame
    except Exception as e:
        st.error(f"Error reading file: {e}")
    
    # SQL query input
    query = st.text_area("Enter your SQL query:", "SELECT * FROM df LIMIT 10")
    
    # Execute the query
    if st.button("Run Query"):
        result = run_query(query, df)
        if isinstance(result, pd.DataFrame):
            st.write("Query Results:")
            st.dataframe(result)  # Display query results
        else:
            st.error(result)
