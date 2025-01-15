import sqlite3
import streamlit as st
import pandas as pd

# Function to create a new SQLite database dynamically based on the Excel file structure
def create_db_from_dataframe(df):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Create table based on the columns of the dataframe
    columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS data_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns}
        )
    ''')
    conn.commit()
    conn.close()

# Insert multiple rows from a DataFrame into the database
def insert_dataframe_to_db(df):
    try:
        conn = sqlite3.connect("database.db")
        df.to_sql('data_table', conn, if_exists='append', index=False)
        conn.close()
        st.success("Data from Excel file uploaded successfully!")
    except Exception as e:
        st.error(f"Error inserting data from Excel: {str(e)}")

# Query data from database
def query_data(filters):
    try:
        conn = sqlite3.connect("database.db")
        query = "SELECT * FROM data_table WHERE 1=1"

        # Apply filters dynamically
        filter_conditions = []
        params = []

        for key, value in filters.items():
            if value:  # If there's a value to filter by
                filter_conditions.append(f'{key} LIKE ?')
                params.append(f'%{value}%')  # Use LIKE with wildcards for partial matching

        if filter_conditions:
            query += " AND " + " AND ".join(filter_conditions)

        # Execute the query with parameters
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error querying data: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Run a custom SQL query
def run_sql_query(query):
    try:
        conn = sqlite3.connect("database.db")
        # Return the result as a pandas DataFrame
        if query.strip().lower().startswith('select'):
            df = pd.read_sql_query(query, conn)
        else:
            conn.execute(query)
            conn.commit()
            df = pd.DataFrame()  # For non-SELECT queries, no result set is returned
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error running SQL query: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Main app
def main():
    st.title("Excel Data Uploader and Query Tool")

    # Tabs for data entry, querying data, and SQL query
    tab1, tab2, tab3 = st.tabs(["📥 Upload Data", "🔎 User Search", "⚙️ SQL Query"])

    # Upload Data Tab
    with tab1:
        st.header("Upload Data")
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

        if uploaded_file is not None:
            try:
                # Read the uploaded Excel file
                df = pd.read_excel(uploaded_file)

                # Check the structure of the DataFrame
                st.write("Preview of the uploaded data:")
                st.dataframe(df.head())

                # Create the database and table based on the uploaded file
                create_db_from_dataframe(df)

                # Upload the data to the database
                if st.button("Upload Data to Database"):
                    insert_dataframe_to_db(df)

            except Exception as e:
                st.error(f"Error reading the Excel file: {str(e)}")

    # User Search Tab (non-SQL)
    with tab2:
        st.header("Search Data")

        if uploaded_file is None:
            st.warning("Please upload a file first to enable searching.")
        else:
            # Fetch the columns from the uploaded data
            filter_columns = pd.read_sql_query("PRAGMA table_info(data_table)", sqlite3.connect("database.db"))
            filter_columns = filter_columns['name'].tolist()

            filters = {}
            for col in filter_columns:
                filters[col] = st.text_input(f"Filter by {col}")

            if st.button("Search"):
                result_df = query_data(filters)
                if not result_df.empty:
                    st.dataframe(result_df)
                else:
                    st.write("No records found.")

    # SQL Query Tab (for advanced users)
    with tab3:
        st.header("Run Custom SQL Query")
        query = st.text_area("Enter SQL Query (e.g., SELECT * FROM data_table)")

        if st.button("Run Query"):
            if query.strip():
                result_df = run_sql_query(query)
                if not result_df.empty:
                    st.dataframe(result_df)
                else:
                    st.write("No data returned or error in query.")
            else:
                st.error("Please enter a SQL query.")

if __name__ == "__main__":
    main()
