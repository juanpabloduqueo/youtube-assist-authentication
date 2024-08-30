import streamlit as st
import lchelper as lch
import textwrap
from dotenv import load_dotenv
import os

load_dotenv()

# User authentication
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    st.error("Please provide a valid username and password")
    st.stop()
    
def authenticate_user(username, password):
    '''
    Authenticate the user with the provided username and password.
    '''
    return username == USERNAME and password == PASSWORD
    
st.title("YouTube Assistant")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Authentication form
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.success("Login verification successful, please click Login again to proceed")
        else:
            st.error("Username/Password is incorrect")
else:
    with st.sidebar:
        with st.form(key='my_form'):
            youtube_url = st.sidebar.text_area("What is the YouTube video URL?", max_chars=50)
            query = st.sidebar.text_area("Ask me about the video?", max_chars=100, key="query")
            language = st.selectbox("Select the language of the video and the response:", ["en", "es", "de"])
            submit_button = st.form_submit_button(label='Submit')       
        
    if submit_button and query and youtube_url:
        db = lch.create_vector_from_youtube_url(youtube_url, language)
        response, doc = lch.get_response_from_query(db, query, language)
        st.subheader("Answer:")
        st.markdown(textwrap.fill(response, width=80))
