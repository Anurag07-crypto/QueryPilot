import streamlit as st
import requests

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
    .user-msg {
        background-color: #DCF8C6;
        color: #000000;  /* 🔥 FIX: dark text */
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
        font-weight: 500;
    }

    .bot-msg {
        background-color: #F1F0F0;
        color: #000000;  /* 🔥 FIX: dark text */
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- HEADER --------------------
st.title("🤖 RAG Chatbot")
st.caption("Ask anything — powered by your RAG pipeline")

# -------------------- CHAT DISPLAY --------------------
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-msg">{chat["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{chat["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INPUT --------------------
query = st.chat_input("Type your message...")

# -------------------- HANDLE INPUT --------------------
if query:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": query})

    with st.spinner("Thinking... 🧠"):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"query": query},
                timeout=30
            )

            if res.status_code == 200:
                data = res.json()
                response = data.get("response", "No response from server")
            else:
                response = f"❌ Error: {res.text}"

        except Exception as e:
            response = f"⚠️ Connection error: {str(e)}"

    # Add bot response
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Rerun to update UI
    st.rerun()

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write("This chatbot uses a RAG pipeline + FastAPI backend.")