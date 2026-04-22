import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Chatbot Luật Lao Động",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #1E88E5;
    border-radius: 10px;
    padding: 10px;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background-color: #2E2E2E;
    border-radius: 10px;
    padding: 10px;
}

textarea {
    background-color: #262730 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Model: RAG + LLM (via FastAPI)")

# header
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
🤖 Chatbot Luật Lao Động Việt Nam
</h1>
""", unsafe_allow_html=True)

# session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
query = st.chat_input("Nhập câu hỏi của bạn...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    with st.spinner("🤖 Đang suy nghĩ..."):
        try:
            response = requests.post(
                API_URL,
                json={"question": query},
                timeout=30
            )

            data = response.json()
            answer = data.get("answer", "Không có câu trả lời")
            docs = data.get("docs", [])

        except Exception as e:
            answer = f"Lỗi kết nối API: {e}"
            docs = []

    with st.chat_message("assistant"):
        st.write(answer)

        if docs:
            st.markdown("**📚 Nguồn:**")
            for doc in docs:
                st.write(f"- {doc.get('title', '')}")

    st.session_state.messages.append({"role": "assistant", "content": answer})
