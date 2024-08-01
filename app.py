# create a new folder
# to create avirtual env--> py -m venv .venv
# to activate the virtual env--> .\.venv\Scripts\activate
# to drop virtual env --> rmdir /s /q .venv
# pip install-->
# streamlit google-generativeai python-dotenv==1.0.1 pdf2image==1.17.0 poppler-utils 0.1.0
# To run the page--> streamlit run app.py

import streamlit as st
import google.generativeai as genai
import os
import base64
import pdf2image
from PIL import Image
import io

# setup api key
genai.configure(api_key= "AIzaSyAuOv1wKhVj_iJzQa5sB9Fp2NOggn1Bvn0")

# design the front end
st.header("Linkedin Profile Analysis & ATS Score")
st.subheader(body="ATS Tracking System & Profile SWOT Anlayis")
input_text= st.text_area(label="Enter the Job Description", key="Input J.D.")

upload_file=st.file_uploader(label="Ipload the Resume",type="pdf")

if upload_file is not None:
    st.write("The File is Uploaded Successfully")
    
# buttons
submit1=st.button("Summary of the Resume")
submit2=st.button("Calculate the ATS Score")


# writing prompts

prompt1= '''Act as a Technical HR and Ops Manager and your task is to review\
    the profile against the Job Description. Please share your personal evaluation\
        including SWOT analysis of the profile with respect to the Job Description.\
            Give me the profile hioghlights in pointers'''

prompt2= '''You are a skileed ATS(Application Tracking system) scanner\
    with a deep understanding of Data Science, Machine Learning and Artificial Intelligence followed\
        by ATS Fucntionality. Your task is to evaluate the resume with the Job Description\
            and give me the percentage match if the resume matches the Job description.\
                The first output should come as ATS Score: in percentage followed by missing\
                    keywords in the resume(in bullet points) and in the end give me a improvement\
                    areas along with your final thoughts'''


# Gen Ai Model..
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# PDF File
def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Convert pdf into Image
        images = pdf2image.convert_from_bytes(upload_file.read())
       
        first_page = images[0]
        # Convert them into Bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Lets put soul into the buttons
if submit1:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemini_response(prompt1,pdf_content,
                                     input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemini_response(prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")
