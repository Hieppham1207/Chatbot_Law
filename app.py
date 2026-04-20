import streamlit as st
from build_RAG import chatbot

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
    st.write("Model: RAG + LLM")

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
        answer, docs = chatbot(query)

    with st.chat_message("assistant"):
        st.write(answer)

        st.markdown("**📚 Nguồn:**")
        for doc in docs:
            st.write(f"- {doc['title']}")

    st.session_state.messages.append({"role": "assistant", "content": answer})