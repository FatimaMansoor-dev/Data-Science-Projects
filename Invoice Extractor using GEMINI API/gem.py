import google.generativeai as genai
import streamlit as st
import os
from PIL import Image 
 

api = 'AIzaSyBUFwHsf_r3u1tLVuBk2z6vxiCG4XkMJcM'
genai.configure(api_key=api)

model = genai.GenerativeModel('models/gemini-pro-vision') 

def get_gemini_resp(inp, image, prompt):  # Corrected the variable name to match the argument list
    response = model.generate_content([inp, image[0], prompt])  # Corrected the variable name to match
    return response.text 

def input_image_details(file):
    if file is not None:
        bytes_data = file.getvalue()

        img = [
            {
                'mime_type': file.type,
                'data' : bytes_data 
            }
        ]

        return img
    else:
        raise FileNotFoundError('No File Uploaded.') 

st.set_page_config(page_title='Invoice extractor')
st.header('Invoice Extractor')
input = st.text_input('Image Prompt :', key='input')
uploaded_file = st.file_uploader('Choose an image.. ', type=['jpg', 'png', 'jpeg']) 
image = ''

submit = st.button('Tell me about invoice.')  # Corrected the assignment of the submit button

input_prompt = 'You are expert in understanding invoices. I will upload an invoice and you will answer me my questions'

if submit:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.sidebar.title("Uploaded Image")
        st.sidebar.image(image, caption='Uploaded image', use_column_width=True)
        img_data = input_image_details(uploaded_file)
        resp = get_gemini_resp(input_prompt, img_data, input)

        st.subheader('Response : ')
        st.write(resp)