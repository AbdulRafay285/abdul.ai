import streamlit as st
import google.generativeai as genai

# --- Streamlit Page Config ---
st.set_page_config(page_title="ABDUL.ai", page_icon="", layout="centered")

# --- Custom CSS for WhatsApp style bubbles ---
st.markdown("""
    <style>
    body {background-color: #F29EF7;} /* Updated Background Color */
    .chat-container {max-width: 600px; margin: auto; padding-bottom: 100px;}
    .message {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 15px;
    }
    .user {
        background-color: #dcf8c6;
        margin-left: auto;
        display: block;
        text-align: right;
    }
    .bot {
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-right: auto;
        display: block;
        text-align: left;
    }
    .sticky-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px;
        border-top: 1px solid #ddd;
        display: flex; gap: 10px; z-index: 1000;
        align-items: center;
    }
    .sticky-bar input {
        flex: 1; border-radius: 20px; border: 1px solid #ccc; padding: 10px 15px;
    }
    .send-btn {
        background-color: #25d366; color: white;
        border: none; border-radius: 50%;
        width: 40px; height: 40px; cursor: pointer; font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Centered Title + Subtitle ---
st.markdown("<h1 style='text-align: center;'>🤖 ABDUL.ai</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>simple message chatbot</p>", unsafe_allow_html=True)

# --- Configure Gemini API ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State for Messages ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display Chat History ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state["messages"]:
    role = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"<div class='message {role}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Sticky Input Bar with Send Button Inside ---
st.markdown('<div class="sticky-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([10,1])
with col1:
    user_input = st.text_input("Type a message...", key="chat_input", label_visibility="collapsed")
with col2:
    send = st.button("➤", key="send_btn")
st.markdown('</div>', unsafe_allow_html=True)

# --- Send Message ---
if send and user_input:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Get bot response
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()



