import streamlit as st
import pandas as pd

st.title("Excel to Queryable Database")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx or .xls)", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Explicitly specify the engine to avoid dependency issues
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.success("File uploaded successfully!")
        
        # Display the data
        st.write("Preview of your data:")
        st.dataframe(df)
        
        # Simple filtering feature
        st.header("Filter your data")
        column = st.selectbox("Select a column to filter by:", df.columns)
        value = st.text_input("Enter a value to filter for:")
        
        if value:
            filtered_df = df[df[column].astype(str).str.contains(value, na=False)]
            st.write("Filtered Results:")
            st.dataframe(filtered_df)

            # Downloadable filtered results
            st.download_button(
                label="Download Filtered Data as CSV",
                data=filtered_df.to_csv(index=False),
                file_name="filtered_data.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Error reading the file: {e}")
