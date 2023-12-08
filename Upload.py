import streamlit as st
import pymongo
from io import BytesIO
import base64

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
db = client['EventDatabase']
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
    
    