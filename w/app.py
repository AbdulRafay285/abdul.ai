import streamlit as st
import google.generativeai as genai

# --- Streamlit Page Config ---
st.set_page_config(page_title="ABDUL.ai", page_icon="🤖", layout="centered")

# --- Sidebar Theme Selector ---
theme = st.sidebar.radio("🌈 Choose Theme", ["Light", "Dark", "Custom"])

# --- Colors for Each Theme ---
if theme == "Light":
    bg_color = "#FFFFFF"
    user_color = "#DCF8C6"   # WhatsApp green
    bot_color = "#FFFFFF"    # White bubble
    bot_border = "#DDD"
elif theme == "Dark":
    bg_color = "#1E1E1E"
    user_color = "#DCF8C6"   # WhatsApp green
    bot_color = "#FFFFFF"    # White bubble
    bot_border = "#444"
else:  # Custom
    bg_color = "#87F1DC"
    user_color = "#B6F7C1"   # Light green
    bot_color = "#FFFFFF"    # White bubble
    bot_border = "#DDD"

# --- Custom CSS with Dynamic Background & Chat Colors ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    .chat-container {{max-width: 600px; margin: auto; padding-bottom: 100px;}}
    .message {{
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 15px;
    }}
    .user {{
        background-color: {user_color};
        margin-left: auto;
        display: block;
        text-align: right;
        color: black;
    }}
    .bot {{
        background-color: {bot_color};
        border: 1px solid {bot_border};
        margin-right: auto;
        display: block;
        text-align: left;
        color: black;
    }}
    .sticky-bar {{
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px;
        border-top: 1px solid #ddd;
        display: flex; gap: 10px; z-index: 1000;
        align-items: center;
    }}
    .sticky-bar input {{
        flex: 1; border-radius: 20px; border: 1px solid #ccc; padding: 10px 15px;
    }}
    .send-btn {{
        background-color: #25d366; color: white;
        border: none; border-radius: 50%;
        width: 40px; height: 40px; cursor: pointer; font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Title & Subtitle Colors based on Theme ---
if theme == "Dark":
    title_color = "white"        # ✅ Dark mode me white
    subtitle_color = "lightgray" # ✅ Dark mode me halka gray
    user_text_color = "white"
    bot_text_color = "white"
elif theme == "Light":
    title_color = "black"
    subtitle_color = "gray"
    user_text_color = "black"
    bot_text_color = "black"
else:  # Custom
    title_color = "black"
    subtitle_color = "gray"
    user_text_color = "black"
    bot_text_color = "black"

# --- Centered Title + Subtitle ---
st.markdown("<h1 style='text-align: center; color:{title_color};'>🤖 ABDUL.ai</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:{subtitle_color};'>simple message chatbot</p>", unsafe_allow_html=True)

# --- Configure Gemini API ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State for Messages ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Function to send message ---
def send_message():
    user_msg = st.session_state.user_input
    if user_msg.strip() == "":
        return
    st.session_state["messages"].append({"role": "user", "content": user_msg})

    try:
        response = model.generate_content(user_msg)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ✅ Clear input safely
    del st.session_state["user_input"]

# --- Display Chat History ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state["messages"]:
    role = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='message {role}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# --- Sticky Input Bar ---
st.markdown('<div class="sticky-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([10,1])

with col1:
    user_input = st.text_input(
        "Type a message...",
        key="user_input",
        label_visibility="collapsed",
        on_change=send_message  # ✅ Enter sends
    )
with col2:
    send = st.button("➤", key="send_btn", on_click=send_message)

st.markdown('</div>', unsafe_allow_html=True)











