import streamlit as st
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import openai
import getpass

# Set the GOOGLE_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = "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"

# Check if GOOGLE_API_KEY is not already set
if "OPENAI_API_KEY" not in os.environ:
    # Prompt for the API key securely
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter Openai API Key: ")



DATA_DIR = "C:/Users/Aditya/Downloads/Data"

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state variables if they don't already exist
if 'index_ready' not in st.session_state:
    st.session_state['index_ready'] = False

st.title("DocChat: Where PDFs Open Up to Conversation")

# Sidebar for file uploads
with st.sidebar:
    uploaded_files = st.file_uploader("Upload your files here", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded PDF to the data directory
            with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("Files Uploaded Successfully")

# Button to index documents, placed in the sidebar
with st.sidebar:
    if st.button("Index your files to get started"):
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        st.session_state['index'] = index  # Store the index in session state
        st.session_state['index_ready'] = True
        st.success("Documents Indexed")

# Main area for query input
st.write("## Ask Your Question Here")
user_query = st.text_input("", key="query_input")

if user_query:
    if st.session_state.get('index_ready', False):
        query_engine = st.session_state['index'].as_query_engine()
        query_response = query_engine.query(user_query)
        response_text = query_response.response
        st.write(response_text)
    else:
        st.error("Please upload and index documents before querying.")
