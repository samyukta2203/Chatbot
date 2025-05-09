import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load API Key
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel("gemini-1.5-flash")

# Toggle state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.markdown("### 🌓 Theme")
st.session_state.dark_mode = st.sidebar.toggle(
    "Dark Mode",
    help="Switch between light and dark background",
    label_visibility="visible"
)

# Define aesthetic colors
bg_color = "#121212" if st.session_state.dark_mode else "#f4f4f4"
text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
chat_bg_user = "#4a90e2" if st.session_state.dark_mode else "#d1e7dd"
chat_bg_bot = "#2c3e50" if st.session_state.dark_mode else "#ffffff"
toggle_color = "#0f62fe" if st.session_state.dark_mode else "#4CAF50"
sidebar_bg_color = "#1a1a1a" if st.session_state.dark_mode else "#ffffff"
sidebar_text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
conversation_text_color = "#ffffff" if st.session_state.dark_mode else "#000000"

# ---------- Custom Styling ----------
st.markdown(f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-family: 'Arial', sans-serif;
    }}
    .title {{
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: 40px;
        padding: 0 15%;
        transition: all 0.3s ease;
    }}
    .chat-box {{
        padding: 14px 18px;
        border-radius: 16px;
        max-width: 75%;
        font-size: 16px;
        word-wrap: break-word;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .user {{
        align-self: flex-end;
        background-color: {chat_bg_user};
        color: #fff;
        text-align: right;
        margin-bottom: 15px;
        transform: translateX(10px);
    }}
    .bot {{
        align-self: flex-start;
        background-color: {chat_bg_bot};
        color: {conversation_text_color};
        text-align: left;
        margin-bottom: 15px;
        transform: translateX(-10px);
    }}
    .recommend-link {{
        display: inline-block;
        margin-top: 10px;
        padding: 8px 14px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-size: 14px;
        transition: background-color 0.3s ease;
    }}
    .recommend-link:hover {{
        background-color: #45a049;
    }}
    [data-testid="stToggle"] .st-bx {{
        background-color: {toggle_color} !important;
    }}
    .sidebar .sidebar-content {{
        background-color: {sidebar_bg_color} !important;
        color: {sidebar_text_color} !important;
    }}
    .sidebar .sidebar-header {{
        font-size: 22px;
        color: {sidebar_text_color};
    }}
    .sidebar .sidebar-content .stTextInput input {{
        color: {sidebar_text_color};
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<div class='title'>AI Furniture Recommendation Chatbot</div>", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("Welcome")
image = Image.open("Gemni/chatbot_logo.png")
st.sidebar.image(image, caption="Chatbot", use_container_width=True)

st.sidebar.markdown("### 💬 Tips")
st.sidebar.info("Ask something like:\n- Suggest a bed for a small room\n- I need a table\n- Show me a comfy sofa")

# ---------- Chat Setup ----------
persona = """
You are a helpful furniture recommendation assistant. Always respond like a friendly advisor and never mention being AI or an API.
"""

furniture_links = {
    "sofa": "https://example.com/sofa",
    "chair": "https://example.com/chair",
    "table": "https://example.com/table",
    "bed": "https://example.com/bed",
    "shelf": "https://example.com/shelf",
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Input ----------
user_input = st.text_input("What furniture are you looking for?", key="input")

if st.button("Ask", use_container_width=True):
    if user_input.strip():
        st.session_state.chat_history.append(("user", user_input))

        prompt = persona + "\nUser: " + user_input
        with st.spinner("Generating recommendation..."):
            response = model.generate_content(prompt)
            reply = response.text

        for key, url in furniture_links.items():
            if key in user_input.lower():
                reply += f"<br><a class='recommend-link' href='{url}' target='_blank'>View {key.title()} Options</a>"
                break

        st.session_state.chat_history.append(("bot", reply))
    else:
        st.warning("Please enter a question first.")

# ---------- Display Chat ----------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    role_class = "user" if sender == "user" else "bot"
    st.markdown(f"<div class='chat-box {role_class}'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
