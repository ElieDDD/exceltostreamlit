import streamlit as st
import pandas as pd
import sqlite3

st.title("Excel File Viewer with SQLite Query Interface")

# Expander 1: File Upload
with st.expander("📄 Upload Excel File", expanded=True):
    st.subheader("Upload Your Excel File")
    uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            st.success("File uploaded and read successfully!")
            st.write("Preview of your data:")
            st.dataframe(df)

            # Save DataFrame to SQLite in-memory database
            conn = sqlite3.connect(":memory:")  # In-memory database
            df.to_sql("uploaded_data", conn, index=False, if_exists="replace")

            st.success("Data loaded into an SQLite database!")
        except ImportError as e:
            st.error("The library 'openpyxl' is required to read Excel files. Please install it by running `pip install openpyxl`.")
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")

# Expander 2: SQL Query Interface
with st.expander("🛠️ SQL Query Interface", expanded=False):
    st.subheader("Run SQL Query on Your Data")

    # Check if data has been uploaded
    if 'df' in locals() and not df.empty:
        # SQL Query Input
        query = st.text_area("Enter your SQL query:", "SELECT * FROM uploaded_data LIMIT 10")

        if st.button("Run Query"):
            try:
                result_df = pd.read_sql_query(query, conn)
                st.write("Query Results:")
                st.dataframe(result_df)

                # Option to download query results
                st.download_button(
                    label="Download Query Results as CSV",
                    data=result_df.to_csv(index=False),
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error executing query: {e}")
    else:
        st.warning("Please upload a file in the '📄 Upload Excel File' section first.")
