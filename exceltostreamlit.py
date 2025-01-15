import streamlit as st
import pandas as pd

# Streamlit app
st.title("Excel to Queryable Database")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read the Excel file into a DataFrame
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Preview of your data:")
        st.dataframe(df)  # Display the DataFrame
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")

    # Querying Interface
    st.header("Query Your Data")

    # Select a column
    column = st.selectbox("Select a column to filter:", df.columns)

    # Input filter value
    value = st.text_input("Enter a value to search for in the selected column:")

    # Apply filter
    if value:
        try:
            filtered_df = df[df[column].astype(str).str.contains(value, na=False, case=False)]
            st.write(f"Filtered Results (Showing rows where `{column}` contains `{value}`):")
            st.dataframe(filtered_df)  # Display the filtered data

            # Option to download results
            st.download_button(
                label="Download Filtered Results as CSV",
                data=filtered_df.to_csv(index=False),
                file_name="filtered_results.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Error while filtering data: {e}")

    # SQL-Like Filter (Optional)
    st.subheader("Advanced: Enter SQL-Like Query (Pandas Syntax)")
    query = st.text_area("Enter a query (e.g., `column_name == 'value'`):")
    if st.button("Run Query"):
        try:
            query_result = df.query(query)
            st.write("Query Results:")
            st.dataframe(query_result)

            # Option to download results
            st.download_button(
                label="Download Query Results as CSV",
                data=query_result.to_csv(index=False),
                file_name="query_results.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Error executing query: {e}")
