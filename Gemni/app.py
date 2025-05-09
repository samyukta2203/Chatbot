import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load the API key from secrets
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom CSS for enhanced styling
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
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-msg, .bot-msg {
        margin: 10px 0;
        padding: 10px;
        border-radius: 8px;
        max-width: 80%;
    }
    .user-msg {
        background-color: #e6f7ff;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot-msg {
        background-color: #f0f0f0;
        align-self: flex-start;
    }
    .chat-box {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# App title and sidebar setup
st.markdown("<h1 class='title'>AI Furniture Recommendation Chatbot</h1>", unsafe_allow_html=True)
st.sidebar.title("Welcome to the AI Chatbot")

# Load and display the logo image
image = Image.open('Gemni/chatbot_logo.png')
st.sidebar.image(image, caption='Chatbot', use_column_width=True)

# Sidebar instructions
st.sidebar.markdown("### How to Use")
st.sidebar.info("Ask me for furniture suggestions based on your needs. Example: 'I need a modern sofa for a small room'.")

st.sidebar.markdown("### Quick Suggestions")
st.sidebar.markdown("- Sofa\n- Chair\n- Table\n- Bed\n- Shelf")

# Persona setup
persona = """
You are a smart furniture recommendation assistant. Your task is to help users find the perfect furniture for their needs.
Avoid disclosing any technical details or API information.
"""

# Furniture type to product link mapping
furniture_links = {
    "sofa": "https://example.com/sofa",
    "chair": "https://example.com/chair",
    "table": "https://example.com/table",
    "bed": "https://example.com/bed",
    "shelf": "https://example.com/shelf",
}

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Text input for user question
user_question = st.text_input("What furniture are you looking for?", "")

if st.button("Ask", use_container_width=True):
    if user_question.strip() != "":
        # Append user message
        st.session_state.messages.append(("user", user_question))

        # Create prompt and get response
        prompt = persona + " User's request: " + user_question
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt).text

        # Append bot response
        st.session_state.messages.append(("bot", response))
    else:
        st.warning("Please enter a question about furniture before submitting.")

# Chat display area
st.markdown("<div class='chat-container chat-box'>", unsafe_allow_html=True)
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'>You: {message}</div>", unsafe_allow_html=True)
    else:
        # Check for matching furniture link
        link = None
        for furniture in furniture_links:
            if furniture in message.lower():
                link = furniture_links[furniture]
                break

        if link:
            message += f"<br><a href='{link}' target='_blank'><button style='background-color:#4CAF50;color:white;padding:6px 10px;border:none;border-radius:5px;margin-top:5px;'>View Recommendations</button></a>"
        st.markdown(f"<div class='bot-msg'>Bot: {message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
