import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load the API key from secrets
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------------- CSS Styling ---------------- #
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 15px;
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .user-msg, .bot-msg {
        padding: 12px 15px;
        border-radius: 10px;
        max-width: 80%;
        line-height: 1.5;
        font-size: 15px;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #d1ecf1;
        align-self: flex-end;
        color: #0c5460;
    }
    .bot-msg {
        background-color: #f8f9fa;
        align-self: flex-start;
        color: #333;
    }
    .chat-input {
        margin-top: 20px;
    }
    a.button-link > button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 6px;
        margin-top: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    a.button-link > button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- App Layout ---------------- #
st.markdown("<div class='title'>AI Furniture Recommendation Chatbot</div>", unsafe_allow_html=True)
st.sidebar.title("Welcome!")

# Sidebar content
image = Image.open('Gemni/chatbot_logo.png')
st.sidebar.image(image, caption='Chatbot', use_column_width=True)

st.sidebar.markdown("### How to Use")
st.sidebar.info("Type your furniture needs. Example:\n'I need a sofa for a small room.'")

st.sidebar.markdown("### Quick Suggestions")
st.sidebar.markdown("- Sofa\n- Chair\n- Table\n- Bed\n- Shelf")

# Persona
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_question = st.text_input("What furniture are you looking for?", key="input")

if st.button("Ask", use_container_width=True):
    if user_question.strip() != "":
        st.session_state.messages.append(("user", user_question))

        prompt = persona + " User's request: " + user_question
        with st.spinner("Thinking..."):
            response_text = model.generate_content(prompt).text

        st.session_state.messages.append(("bot", response_text))
    else:
        st.warning("Please enter your question.")

# ---------------- Chat Display ---------------- #
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'>{message}</div>", unsafe_allow_html=True)
    else:
        # Check for matching furniture type
        link = None
        for furniture in furniture_links:
            if furniture in message.lower():
                link = furniture_links[furniture]
                break

        if link:
            message += f"<br><a href='{link}' target='_blank' class='button-link'><button>View Recommendations</button></a>"
        st.markdown(f"<div class='bot-msg'>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

