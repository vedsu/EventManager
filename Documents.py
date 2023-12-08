import streamlit as st
import pymongo
# import pandas as pd
# import time
from datetime import datetime, timedelta
# import pytz
from io import BytesIO
import base64




@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
        return client
    except Exception as e:
        st.error(f"Error raised, {str(e)}")
    
client = init_connection()
db = client['EventDatabase']
collection = db['Webinars']

def main():
    # Create columns with specified widths
    col1, col2 = st.columns([3, 7])  
            
    with col1:
            st.subheader("Upload document to Webinar")

    
            # Query MongoDB to retrieve webinar data
            webinars = collection.find({"Webinar": {"$ne": "Holiday"}, "Status": {"$ne": "Completed"}})
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
                    st.sidebar.error(f'Failed!: {str(e)}')           # st.caption(pdf_href, unsafe_allow_html=True)
    with col2:
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
            date = event.get("Date")
            # Convert the string to a datetime object
            original_date = datetime.strptime(date, "%Y-%m-%d")
                
            # Format the datetime object as a string with the desired format
            formatted_date_string = original_date.strftime("%d-%m-%Y")
            if status!="Completed":
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
                        
                        # st.caption(f"{count} - {formatted_date_string} : {webinar} : {pdf_href}", unsafe_allow_html=True)
                        st.caption( f"<span style='color: black; font-weight: bold;'>{count}</span> - " 
                                    f"<span style='color: blue;'>{formatted_date_string}</span> : "
                                    f"<span style='font-weight: bold;'>{webinar}</span> : "
                                    f"<a href='{pdf_href}' style='color: red;' target='_blank'>{pdf_href}</a>",unsafe_allow_html=True)
