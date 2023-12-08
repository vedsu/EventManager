import streamlit as st
import pymongo
from io import BytesIO
import base64

# Connect to MongoDB
# client = pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
# db = client['EventDatabase']
# collection = db['Webinars']
#Database Connections
@st.cache_resource
def init_connection():
    try:
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password

        mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        client = pymongo.MongoClient(mongo_uri)
        # # mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/
        # client=pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
        return client
    except:
        st.write("Connection Could not be Established with database")

client = init_connection()
db= client['EventDatabase']

collection = db['Webinars']

# Streamlit app
def main():
    st.title("Upload document to Webinar")

    
    # Query MongoDB to retrieve webinar data
    webinars = collection.find({"Webinar": {"$ne": "Holiday"}})
    # Extract webinar titles from the query result
    webinar_titles = ["Select Webinar Title"] + [webinar["Webinar"] for webinar in webinars]
    # Streamlit app
    selected_webinar_title = st.selectbox("Select Webinar Title", webinar_titles)

    # Display selected webinar title
    st.write(f"Selected Webinar Title: {selected_webinar_title}")
    # File upload
    
    uploaded_file = st.file_uploader("Choose a PDF file")

    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        # Read PDF content
        pdf_content = BytesIO(uploaded_file.read())
        document = pdf_content.read()

    
        try:
            result = collection.update_one(
                        {"Webinar": selected_webinar_title},
                            {"$set": {"Document": document}})
            if result:
                st.info(f"File inserted into MongoDB with Name: {selected_webinar_title}")
            else:
                st.info(f"File could not be inserted into MongoDB with Name: {selected_webinar_title}")

        except Exception as e:
            st.sidebar.error(f'Failed!: {str(e)}')
    
    
