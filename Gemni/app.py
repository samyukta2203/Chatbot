import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load the API key from secrets
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------- Custom CSS Styling ----------
st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .user-msg, .bot-msg {
        padding: 12px 16px;
        border-radius: 10px;
        max-width: 85%;
        line-height: 1.6;
        font-size: 15px;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    .user-msg {
        background-color: #e0f7fa;
        align-self: flex-end;
        color: #000;
        border: 1px solid #00bcd4;
    }
    .bot-msg {
        background-color: #f1f1f1;
        align-self: flex-start;
        color: #000;
        border: 1px solid #ddd;
    }
    .button-container {
        margin-top: 10px;
    }
    .recommend-btn {
        background-color: #4CAF50;
        color: white;
        padding: 8px 14px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        text-decoration: none;
    }
    .recommend-btn:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Page Title ----------
st.markdown("<div class='title'>AI Furniture Recommendation Chatbot</div>", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("Welcome!")

image = Image.open('Gemni/chatbot_logo.png')
st.sidebar.image(image, caption='Chatbot', use_container_width=True)

st.sidebar.markdown("### How to Use")
st.sidebar.info("Ask me furniture-related questions. For example:\n'I need a table for my study room.'")

st.sidebar.markdown("### Suggestions")
st.sidebar.markdown("- Sofa\n- Chair\n- Table\n- Bed\n- Shelf")

# ---------- Persona ----------
persona = """
You are a smart furniture recommendation assistant. Your task is to help users find the perfect furniture for their needs.
Avoid disclosing any technical details or API information.
"""

# ---------- Furniture Links ----------
furniture_links = {
    "sofa": "https://example.com/sofa",
    "chair": "https://example.com/chair",
    "table": "https://example.com/table",
    "bed": "https://example.com/bed",
    "shelf": "https://example.com/shelf",
}

# ---------- Session Storage ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Input ----------
user_question = st.text_input("What furniture are you looking for?", key="chat_input")

if st.button("Ask", use_container_width=True):
    if user_question.strip() != "":
        st.session_state.messages.append(("user", user_question))

        prompt = persona + " User's request: " + user_question
        with st.spinner("Thinking..."):
            response_text = model.generate_content(prompt).text

        st.session_state.messages.append(("bot", response_text))
    else:
        st.warning("Please enter your question.")

# ---------- Chat Display ----------
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

        # Append the link if found
        if link:
            message += f"<div class='button-container'><a href='{link}' target='_blank' class='recommend-btn'>View Recommendations</a></div>"

        st.markdown(f"<div class='bot-msg'>{message}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
