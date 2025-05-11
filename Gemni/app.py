import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load API Key
api_key = st.secrets["GOOGLE_API_KEY"]
model = genai.GenerativeModel("gemini-1.5-flash")

# Toggle state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.markdown("## 🛠️ Settings")
st.session_state.dark_mode = st.sidebar.toggle(
    "🌗 Dark Mode",
    help="Switch between light and dark theme",
    label_visibility="visible"
)

# Theme-dependent variables
bg_color = "#f4f4f4" if not st.session_state.dark_mode else "#1c1c1c"
text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
chat_bg_user = "#00796b" if not st.session_state.dark_mode else "#009688"
chat_bg_bot = "#e0e0e0" if not st.session_state.dark_mode else "#333333"
sidebar_bg_color = "#ffffff" if not st.session_state.dark_mode else "#1a1a1a"
sidebar_text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
conversation_text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
button_bg_color = "#00796b" if not st.session_state.dark_mode else "#009688"
button_text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
input_bg_color = "#ffffff" if not st.session_state.dark_mode else "#333333"
input_text_color = "#000000" if not st.session_state.dark_mode else "#ffffff"
input_label_color = "#000000" if not st.session_state.dark_mode else "#ffffff"

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
        background-color: #00574B;
    }}
    label {{
        color: {input_label_color} !important;
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
    .custom-submit {{
        background-color: {button_bg_color};
        color: {button_text_color};
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        width: 100%;
        margin-top: 15px;
    }}
    .custom-submit:hover {{
        opacity: 0.9;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<div class='title'>🛋️ FurniMate – Your Furniture Advisor</div>", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("### 🤖 About")
image = Image.open("Gemni/chatbot_logo.png")
st.sidebar.image(image, caption="FurniMate Logo", use_container_width=True)
st.sidebar.info("FurniMate is your smart assistant for personalized furniture suggestions. Just ask!")

st.sidebar.markdown("### 💡 Try Asking:")
st.sidebar.markdown("""
- 🛏️ Suggest a bed for a small room  
- 🪑 I need a comfy chair  
- 🛋️ Show me sofas  
- 📚 Recommend a bookshelf
""")

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

# ---------- Custom Submit Button ----------
submit_html = f"""
<form action="" method="post">
    <input type="hidden" name="submit_trigger" value="1">
    <button class="custom-submit" type="submit">Ask</button>
</form>
"""
st.markdown(submit_html, unsafe_allow_html=True)

# ---------- Handle Submission ----------
if st.session_state.get("submit_trigger", False):
    st.session_state.submit_trigger = False

if "submit_trigger" not in st.session_state:
    st.session_state.submit_trigger = False

# Use query param workaround to detect button click
if st.requested_url_query.get("submit_trigger") == "1" or st.session_state.submit_trigger:
    st.session_state.submit_trigger = True
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
