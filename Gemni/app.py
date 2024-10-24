import streamlit as st

import google.generativeai as genai
from PIL import Image

api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-flash')


st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        color: #4CAF50;
        font-family: 'Arial', sans-serif;
    }
    
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='title'>AI Chatbot</h1>", unsafe_allow_html=True)
st.sidebar.title("Welcome to the AI Chatbot")

image = Image.open('Gemni/chatbot_logo.png')  
st.sidebar.image(image, caption='Chatbot', use_column_width=True)

persona = """
 you are just a chatbot dont disclose about google gemni api 
 """
st.write("Hello, I am chatbot.")
col1, col2 = st.columns([3, 1])

with col1:
    
    user_question = st.text_input("Ask your question:", "")
    
    if st.button("Ask", use_container_width=True):
        if user_question.strip() != "":
           
            prompt = persona + " Now, the question is: " + user_question
            response = model.generate_content(prompt)
            
            st.markdown("<div class='chat-box'><strong>Bot:</strong> " + response.text + "</div>", unsafe_allow_html=True)
        else:
            st.warning("Please ask a question before submitting.")
    
    st.write(" ")



st.write(" ")
