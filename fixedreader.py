import pandas as pd
import streamlit as st
from io import BytesIO
import openpyxl  # Ensure openpyxl is installed (pip install openpyxl)

# Function to read data from a single Excel file, handling potential errors
def read_excel_data(file_data):
    try:
        df = pd.read_excel(BytesIO(file_data), engine='openpyxl')  # Use openpyxl for reliable reading
        df.dropna(subset=['Email'], inplace=True)  # Drop rows with missing emails (optional)
        return df
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return pd.DataFrame()

# Function to read data from multiple Excel files
def read_trainer_data(file_list):
    df_list = []
    for uploaded_file in file_list:
        df = read_excel_data(uploaded_file.getbuffer())  # Read each file using read_excel_data
        if not df.empty:
            df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

# Function to find trainer by name or email with validation
def find_trainer(df, name=None, email=None):
    if name:
        filtered_df = df[df['Name'].str.contains(name, na=False, case=False)]
    elif email:
        # Basic email validation (can be enhanced)
        if '@' not in email or '.' not in email:
            st.warning("Please enter a valid email address.")
            return pd.DataFrame()
        filtered_df = df[df['Email'].str.contains(email, na=False, case=False)]
    else:
        filtered_df = pd.DataFrame()
    return filtered_df

# Streamlit app
def main():
    st.title("Trainer Engagement Processor")

    # File upload
    uploaded_files = st.file_uploader("Upload Excel files (XLSX format only)", accept_multiple_files=True, type="xlsx")
    if uploaded_files:
        file_list = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".xlsx"):
                file_list.append(uploaded_file)
            else:
                st.warning(f"File '{uploaded_file.name}' is not a valid Excel file (XLSX).")

        if file_list:
            df = read_trainer_data(file_list)

            # Search for trainer by name or email
            st.sidebar.header("Search Criteria")
            name = st.sidebar.text_input("Name")
            email = st.sidebar.text_input("Email")

            filtered_df = find_trainer(df.copy(), name=name, email=email)  # Avoid modifying original df

            # Show filtered data (optional)
            # st.subheader("Filtered Data")
            # st.write(filtered_df)

            if not filtered_df.empty:
                selected_row = filtered_df.iloc[0]
                name = selected_row.get('Name', 'N/A')
                email = selected_row.get('Email', 'N/A')
                ttt_status = selected_row.get('TTT Status', 'N/A')

                st.subheader("Trainer Details")
                st.text(f"Name: {name}")
                st.text(f"Email: {email}")
                st.text(f"TTT Status: {ttt_status}")

if __name__ == "__main__":
    main()