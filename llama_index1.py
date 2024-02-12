import streamlit as st
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import openai
import getpass
from dotenv import load_dotenv

load_dotenv()
os.getenv("OPENAI_API_KEY")

# Check if GOOGLE_API_KEY is not already set
if "OPENAI_API_KEY" not in os.environ:
    # Prompt for the API key securely
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter Openai API Key: ")



DATA_DIR = "/home/ubuntu/aditya/DocChat/data"

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize session state variables if they don't already exist
if 'index_ready' not in st.session_state:
    st.session_state['index_ready'] = False

st.title("DocChat:where pdfs open up to conversation ")

# Sidebar for file uploads
with st.sidebar:
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded PDF to the data directory
            with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("Files Uploaded Successfully")

# Button to index documents, placed in the sidebar
with st.sidebar:
    if st.button("Index Documents"):
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        st.session_state['index'] = index  # Store the index in session state
        st.session_state['index_ready'] = True
        st.success("Documents Indexed")

# Main area for query input
st.write("## Enter Your Question Here")
user_query = st.text_input("", key="query_input")

if user_query:
    if st.session_state.get('index_ready', False):
        query_engine = st.session_state['index'].as_query_engine()
        query_response = query_engine.query(user_query)
        response_text = query_response.response
        st.write(response_text)
    else:
        st.error("Please upload and index documents before querying.")




# import boto3
# import streamlit as st

# # Initialize a boto3 client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
# )

# BUCKET_NAME = 'your-bucket-name'  # Replace with your bucket name

# def upload_file_to_s3(file, bucket_name, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file: File to upload
#     :param bucket_name: Bucket to upload to
#     :param object_name: S3 object name. If not specified, file.name is used
#     :return: True if file was uploaded, else False
#     """
#     if object_name is None:
#         object_name = file.name
#     try:
#         s3_client.upload_fileobj(file, bucket_name, object_name)
#     except Exception as e:
#         print(e)
#         return False
#     return True

# with st.sidebar:
#     uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             if upload_file_to_s3(uploaded_file, BUCKET_NAME, uploaded_file.name):
#                 st.success(f"File {uploaded_file.name} uploaded successfully to S3.")
#             else:
#                 st.error(f"Failed to upload {uploaded_file.name}.")
# def read_files_from_s3(bucket_name):
#     """Generate file-like objects from S3 bucket contents."""
#     s3_resource = boto3.resource('s3')
#     bucket = s3_resource.Bucket(bucket_name)
#     for obj in bucket.objects.all():
#         file_content = obj.get()['Body'].read()
#         yield file_content  # Adjust according to how your indexing mechanism consumes files

# # Example usage
# if st.button("Index Documents"):
#     documents = read_files_from_s3(BUCKET_NAME)
#     # Assuming your indexing function can handle a stream of file contents
#     index = VectorStoreIndex.from_documents(documents)
#     st.session_state['index'] = index  # Store the index in session state
#     st.session_state['index_ready'] = True
#     st.success("Documents Indexed")
