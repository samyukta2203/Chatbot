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
bg_color = "#f4f4f4" if not st.session_state.dark_mode else "#1c1c1c"
text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
chat_bg_user = "#00796b" if not st.session_state.dark_mode else "#009688"
chat_bg_bot = "#e0e0e0" if not st.session_state.dark_mode else "#333333"
toggle_color = "#0f62fe" if st.session_state.dark_mode else "#4CAF50"
sidebar_bg_color = "#ffffff" if not st.session_state.dark_mode else "#1a1a1a"
sidebar_text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
conversation_text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
button_bg_color = "#00796b" if not st.session_state.dark_mode else "#009688"
button_hover_color = "#45a049" if st.session_state.dark_mode else "#1E3A8A"
button_text_color = "#ffffff"
input_bg_color = "#ffffff" if not st.session_state.dark_mode else "#333333"
input_text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"

# ---------- Custom Styling ----------
st.markdown(f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-family: 'Arial', sans-serif;
    }}
    .title {{
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 40px;
        padding: 0 15%;
    }}
    .chat-box {{
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 70%;
        font-size: 16px;
        word-wrap: break-word;
        line-height: 1.6;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    .user {{
        align-self: flex-end;
        background-color: {chat_bg_user};
        color: white;
        text-align: right;
        border-radius: 20px 20px 0 20px;
    }}
    .bot {{
        align-self: flex-start;
        background-color: {chat_bg_bot};
        color: {conversation_text_color};
        text-align: left;
        border-radius: 20px 20px 20px 0;
    }}
    .recommend-link {{
        display: inline-block;
        margin-top: 10px;
        padding: 8px 14px;
        background-color: {button_bg_color};
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 14px;
    }}
    .recommend-link:hover {{
        background-color: {button_hover_color};
    }}
    .ask-button {{
        background: {button_bg_color};
        color: {button_text_color};
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        text-transform: uppercase;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }}
    .ask-button:hover {{
        background-color: {button_hover_color};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    .ask-button:active {{
        transform: scale(0.98);
    }}
    .ask-button:focus {{
        outline: none;
    }}
    .stTextInput input {{
        background-color: {input_bg_color} !important;
        color: {input_text_color} !important;
        border-radius: 12px;
        padding: 12px 15px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
    }}
    .stTextInput input:focus {{
        box-shadow: 0 0 5px {button_bg_color};
        outline: none;
    }}
    .sidebar .sidebar-content {{
        background-color: {sidebar_bg_color} !important;
        color: {sidebar_text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<div class='title'>Furniture Recommendation Chatbot</div>", unsafe_allow_html=True)

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

# ---------- Ask Button ----------
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
