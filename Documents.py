import streamlit as st
import pymongo
# import pandas as pd
# import time
from datetime import datetime, timedelta
# import pytz
# from io import BytesIO
import base64


@st.cache_resource
def init_connection():
    try:
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password

        mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        client = pymongo.MongoClient(mongo_uri)
        # client = pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
        return client
    except Exception as e:
        st.error(f"Error raised, {str(e)}")
    
client = init_connection()
db = client['EventDatabase']
collection = db['Webinars']

def main():
    st.subheader("Document Viewer")
    try:
        # Perform the update
        events = collection.find({}).sort("Date", pymongo.ASCENDING)

        # st.write(events)
    except Exception as e:
        st.error(f"Error {str(e)}")
    col1, col2=st.columns(2)
    count=0
    for event in events:
        webinar = event.get("Webinar")
        status = event.get('Status')
        document = event.get("Document")
        if document !=None:
            # Display PDF content as a link
            pdf_content_b64 = base64.b64encode(document).decode('utf-8')
            pdf_href = f'<a href="data:application/pdf;base64,{pdf_content_b64}" target="_blank">View PDF</a>'
        else:
            pdf_href = None


        if webinar!="Holiday":
            count+=1
            with col1:
                # Extract the part before the first occurrence of '-' or ':'
                
                st.caption(f"{count} . {webinar} : {pdf_href}", unsafe_allow_html=True)
            
                # st.caption(pdf_href, unsafe_allow_html=True)
