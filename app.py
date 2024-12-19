import streamlit as st
from modules.data_processing import process_uploaded_files
from modules.search import get_answer

# Initialize Streamlit App
st.title("AI Chat with PDF Knowledge Base")

# Upload PDFs
uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type="pdf")
if uploaded_files:
    if st.button("Process Documents"):
        st.write("Processing uploaded files...")
        process_uploaded_files(uploaded_files)  # Clear and process files

# Chat Interface
query = st.text_input("Ask a question about the uploaded PDFs:")
if st.button("Submit"):
    response = get_answer(query)
    st.write("Response:", response)
