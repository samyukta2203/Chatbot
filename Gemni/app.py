import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load API Key
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel("gemini-1.5-flash")

# Toggle state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar settings toggle
st.sidebar.markdown("## 🛠️ Settings")
st.session_state.dark_mode = st.sidebar.toggle(
    "🌗 Dark Mode",
    help="Switch between light and dark theme",
    label_visibility="visible"
)

# Theme variables
dark_mode = st.session_state.dark_mode
bg_color = "#1c1c1c" if dark_mode else "#f4f4f4"
text_color = "#ffffff" if dark_mode else "#000000"
chat_bg_user = "#009688" if dark_mode else "#00796b"
chat_bg_bot = "#333333" if dark_mode else "#e0e0e0"
conversation_text_color = "#ffffff" if dark_mode else "#000000"
button_bg_color = "#009688" if dark_mode else "#000000"
button_hover_color = "#FF0000"  # Red hover
ask_button_label_color = "#00FF00"  # Green text
input_label_color = "#ffffff" if dark_mode else "#000000"
input_bg_color = "#333333" if dark_mode else "#ffffff"
input_text_color = "#ffffff" if dark_mode else "#000000"
sidebar_bg_color = "#1a1a1a" if dark_mode else "#ffffff"
sidebar_text_color = "#ffffff" if dark_mode else "#000000"

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
        gap: 20px;
        margin-top: 40px;
        padding: 0 10%;
    }}
    .chat-box {{
        padding: 12px 18px;
        border-radius: 16px;
        font-size: 16px;
        word-wrap: break-word;
        line-height: 1.6;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: fit-content;
    }}
    .user {{
        align-self: flex-end;
        background-color: {chat_bg_user};
        color: white;
        text-align: right;
        border-radius: 20px 20px 0 20px;
        margin-left: auto;
    }}
    .bot {{
        align-self: flex-start;
        background-color: {chat_bg_bot};
        color: {conversation_text_color};
        text-align: left;
        border-radius: 20px 20px 20px 0;
        margin-right: auto;
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
        background-color: {button_bg_color};
        color: {ask_button_label_color} !important;
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        transition: background 0.3s, transform 0.2s;
        margin-top: 15px;
        width: 100%;
    }}
    .ask-button:hover {{
        background-color: {button_hover_color};
        transform: scale(1.02);
        color: #ffffff !important;
    }}
    .ask-button:active {{
        transform: scale(0.97);
    }}
    .stTextInput input {{
        background-color: {input_bg_color} !important;
        color: {input_text_color} !important;
        border-radius: 12px;
        padding: 12px 15px;
        border: none;
        font-size: 16px;
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
st.markdown("<div class='title'>🛋️ FurniMate – Your Furniture Advisor</div>", unsafe_allow_html=True)

# ---------- Sidebar ----------
image = Image.open("Gemni/chatbot_logo.png")
st.sidebar.image(image, use_container_width=True)  # Logo above welcome text

st.sidebar.markdown("""
**Welcome to FurniMate!**  
Your home’s new best friend in furniture shopping. ✨  

**How it works:**  
Simply ask, and let FurniMate’s smart AI work its magic, bringing personalized furniture suggestions right to your fingertips. It's like having a personal shopper who knows exactly what your home needs. 🛋️💡
""")

st.sidebar.info("FurniMate is your smart assistant for personalized furniture suggestions. Just ask!")

st.sidebar.markdown("### 💡 Try Asking:")
st.sidebar.markdown("""
- Suggest a cozy sofa for a living room  
- I need a stylish desk  
- Recommend a comfortable bed for a small room  
- Show me trendy bookshelves
""")

# Chat persona
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

# ---------- Input Label ----------
st.markdown(f"<label style='color:{input_label_color}; font-weight:bold; font-size:16px;'>What furniture are you looking for?</label>", unsafe_allow_html=True)
user_input = st.text_input("", key="input", label_visibility="collapsed")

# ---------- Ask Button ----------
if st.button("Ask", key="ask_btn", use_container_width=True):
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
