# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Background image */
    body {
        background-image: url('https://images.unsplash.com/photo-1484417894907-623942c8ee29?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Main container */
    .main {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Main title styling */
    h1 {
        color: #4F8BF9;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 20px;
    }

    /* Subheader styling */
    h2 {
        color: #2E86C1;
        font-size: 2rem;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Button styling */
    .stButton button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1rem;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #2E86C1;
    }

    /* File uploader styling */
    .stFileUploader {
        margin-bottom: 20px;
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Success message styling */
    .stSuccess {
        background-color: #D5F5E3;
        color: #145A32;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }

    /* Error message styling */
    .stError {
        background-color: #FADBD8;
        color: #922B21;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }

    /* Custom card styling */
    .card {
        background-color: #F4F6F6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# JavaScript for interactivity (optional)
st.markdown(
    """
    <script>
    // Example: Add a simple alert when the page loads
    window.onload = function() {
        alert("Welcome to Data Sweeper! 🚀");
    };
    </script>
    """,
    unsafe_allow_html=True,
)

# Set up your App
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1>Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 1.2rem; color: #666;'>Transform your files between CSV and Excel formats with built-in data cleaning and visualization!</p>",
    unsafe_allow_html=True,
)

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"],
                                  accept_multiple_files=True)

def get_file_extension(file):
    file_ext = os.path.splitext(file.name)[-1].lower()
    return file_ext

if uploaded_files:
    for file in uploaded_files:
        file_ext = get_file_extension(file)
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')  # Use openpyxl for Excel files
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        # Display info about the file in a card
        st.markdown(
            f"""
            <div class="card">
                <h3>File Details</h3>
                <p><strong>File Name:</strong> {file.name}</p>
                <p><strong>File Size:</strong> {file.size / 1024:.2f} KB</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Show 5 rows of our dataframe
        st.markdown("<h2>Preview the Head of the Dataframe</h2>", unsafe_allow_html=True)
        st.dataframe(df.head())
        
        # Options for data cleaning
        st.markdown("<h2>Data Cleaning Options</h2>", unsafe_allow_html=True)
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed!")
            
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values have been Filled!")
        
        # Choose specific columns to keep or convert
        st.markdown("<h2>Select Columns to Convert</h2>", unsafe_allow_html=True)
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        # Create some visualizations
        st.markdown("<h2>Data Visualization</h2>", unsafe_allow_html=True)
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        # Convert the file (CSV to Excel or vice versa)
        st.markdown("<h2>Conversion Options</h2>", unsafe_allow_html=True)
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Use openpyxl for Excel files
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            
            # Download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
    
    st.markdown("<div class='stSuccess'>All files processed! 🎉</div>", unsafe_allow_html=True)

# Close the main container
st.markdown("</div>", unsafe_allow_html=True)