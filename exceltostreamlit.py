import sqlite3
import streamlit as st
import pandas as pd

# Function to create a new SQLite database dynamically based on the Excel file structure
def create_db_from_dataframe(df):
    conn = sqlite3.connect("university_data.db")
    cursor = conn.cursor()
    # Create table based on the columns of the dataframe
    columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
    cursor.execute(f''' 
        CREATE TABLE IF NOT EXISTS university_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns}
        )
    ''')
    conn.commit()
    conn.close()

# Insert multiple rows from a DataFrame into the database
def insert_dataframe_to_db(df):
    try:
        conn = sqlite3.connect("university_data.db")
        df.to_sql('university_data', conn, if_exists='append', index=False)
        conn.close()
        st.success("Data from Excel file uploaded successfully!")
    except Exception as e:
        st.error(f"Error inserting data from Excel: {str(e)}")

# Query data from database
def query_data(filters):
    try:
        conn = sqlite3.connect("university_data.db")
        query = "SELECT * FROM university_data WHERE 1=1"

        # Apply filters dynamically
        for key, value in filters.items():
            if value:
                query += f" AND {key} LIKE ?"

        # Execute the query with parameters
        params = tuple(value for value in filters.values() if value)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error querying data: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Run a custom SQL query
def run_sql_query(query):
    try:
        conn = sqlite3.connect("university_data.db")
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
    st.title("Data Schools Database")

    # Tabs for data entry, querying data, and SQL query
    tab1, tab2, tab3 = st.tabs(["📥 Add Data", "🔎 Query Data", "⚙️ SQL Query"])

    # Add Data Tab
    with tab1:
        st.header("Add Data")
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

    # Query Data Tab
    with tab2:
        st.header("Query Data")
        st.write("Use the filters below to search the database:")

        filter_columns = pd.read_sql_query("PRAGMA table_info(university_data)", sqlite3.connect("university_data.db"))
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

    # SQL Query Tab
    with tab3:
        st.header("Run Custom SQL Query")
        query = st.text_area("Enter SQL Query (e.g., SELECT * FROM university_data)")

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
