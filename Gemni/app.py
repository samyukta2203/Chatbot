import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load the API key from secrets
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom styling for the Streamlit app
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

# App title and sidebar setup
st.markdown("<h1 class='title'>AI Recommendation Chatbot</h1>", unsafe_allow_html=True)
st.sidebar.title("Welcome to the AI Chatbot")

# Load and display the logo image
image = Image.open('Gemni/chatbot_logo.png')  
st.sidebar.image(image, caption='Chatbot', use_column_width=True)

# Persona setup for the chatbot
persona = """
You are a smart furniture recommendation assistant. Your task is to help users find the perfect furniture for their needs.
Avoid disclosing any technical details or API information.
"""

# A simple mapping of furniture types to product links
furniture_links = {
    "sofa": "https://example.com/sofa",
    "chair": "https://example.com/chair",
    "table": "https://example.com/table",
    "bed": "https://example.com/bed",
    "shelf": "https://example.com/shelf",
}

# User interaction setup
st.write("Hello! I am your furniture recommendation assistant.")
col1, col2 = st.columns([3, 1])

with col1:
    user_question = st.text_input("What furniture are you looking for?", "")
    
    if st.button("Ask", use_container_width=True):
        if user_question.strip() != "":
            # Create a prompt based on user input
            prompt = persona + " User's request: " + user_question
            # Generate a response from the model
            response = model.generate_content(prompt)

            # Check if the user's question matches any furniture type in the mapping
            link = None
            for furniture in furniture_links.keys():
                if furniture in user_question.lower():
                    link = furniture_links[furniture]
                    break

            # Display the chatbot response
            if link:
                st.markdown("<div class='chat-box'><strong>Bot:</strong> " + response.text + f" You can check out this link for more options: <a href='{link}' target='_blank'>View here</a></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='chat-box'><strong>Bot:</strong> " + response.text + "</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question about furniture before submitting.")
    
    st.write(" ")

st.write(" ")
