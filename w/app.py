import streamlit as st
import google.generativeai as genai

# --- Theme Selector ---
theme = st.sidebar.radio("🌈 Choose Theme", ["Light", "Dark", "Custom"])

if theme == "Light":
    bg_color, user_color, bot_color, bot_border = "#FFFFFF", "#DCF8C6", "#FFFFFF", "#DDD"
elif theme == "Dark":
    bg_color, user_color, bot_color, bot_border = "#1E1E1E", "#056162", "#2A2A2A", "#444"
else:  # Custom
    bg_color, user_color, bot_color, bot_border = "#87F1DC", "#B6F7C1", "#FFFFFF", "#DDD"

# --- Colors for Titles & Messages ---
if theme == "Dark":
    title_color = "white"
    subtitle_color = "lightgray"
    user_text_color = "white"
    bot_text_color = "white"
else:
    title_color = "black"
    subtitle_color = "gray"
    user_text_color = "black"
    bot_text_color = "black"

# --- CSS ---
st.markdown(f"""
    <style>
    .stApp {{background-color: {bg_color};}}
    .chat-container {{max-width: 600px; margin: auto; padding-bottom: 100px;}}
    .message {{
        padding: 10px 15px; border-radius: 20px; margin: 10px;
        display: inline-block; max-width: 80%; word-wrap: break-word; font-size: 15px;
    }}
    .user {{
        background-color: {user_color};
        margin-left: auto;
        display: block;
        text-align: right;
        color: {user_text_color};
    }}
    .bot  {{
        background-color: {bot_color};
        border: 1px solid {bot_border};
        margin-right: auto;
        display: block;
        text-align: left;
        color: {bot_text_color};
    }}
    .sticky-bar {{
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px;
        border-top: 1px solid #ddd;
        display: flex; gap: 10px; z-index: 1000; align-items: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown(f"<h1 style='text-align: center; color:{title_color};'>ABDUL.ai</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size:18px; color:{subtitle_color};'>simple message chatbot</p>", unsafe_allow_html=True)

# --- Gemini API ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""
if "input_reset" not in st.session_state:
    st.session_state["input_reset"] = False

# --- Show Chat History ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state["messages"]:
    role = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"<div class='message {role}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ✅ Auto Scroll to Bottom ---
st.markdown("""
    <script>
    var chatContainer = window.parent.document.querySelector('.main');
    if (chatContainer) {
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    }
    </script>
""", unsafe_allow_html=True)

# --- Function to Send Message ---
def send_message():
    user_msg = st.session_state.chat_input.strip()
    if user_msg == "":
        return

    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_msg})

    # Get bot response
    try:
        response = model.generate_content(user_msg)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ✅ Safe flag to clear input later
    st.session_state.input_reset = True

# --- Sticky Input Bar ---
st.markdown('<div class="sticky-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([10,1])

with col1:
    user_input = st.text_input(
        "Type a message...",
        key="chat_input",
        label_visibility="collapsed",
        on_change=send_message,  # ✅ Enter dabane par bhej do
    )

    # ✅ Reset input safely after widget render
    if st.session_state.input_reset:
        st.session_state.chat_input = ""
        st.session_state.input_reset = False

with col2:
    if st.button("➤"):
        send_message()

st.markdown('</div>', unsafe_allow_html=True)















