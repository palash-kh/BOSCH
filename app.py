import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import os
import streamlit

# Load environment variables from .env file
load_dotenv()
# ----------------------------
# 🔑 Azure OpenAI credentials
# ----------------------------
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY") or st.secrets["AZURE_OPENAI_KEY"]  
DEPLOYMENT_NAME = "gpt-35-turbo-0125-ft-610877ae39ff4995b94346d1147748dd"

# ----------------------------
# ⚙️ Setup Azure client
# ----------------------------
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-05-01-preview",   # latest supported version
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# ----------------------------
# 🎨 Streamlit UI Configuration
# ----------------------------
st.set_page_config(page_title="Bosch Customer Support", page_icon="💬", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #dbeafe;
        text-align: right;
    }
    .stChatMessage.assistant {
        background-color: #f3f4f6;
    }
    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 30px;
        color: #6b7280;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 📌 Header with Bosch Logo
# ----------------------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("image.png", width=100)
with col2:
    st.title("Bosch Customer Support Chatbot")
    st.write("🤖 Helping you with product inquiries, warranty, and troubleshooting.")

# ----------------------------
# 📌 Sidebar with Quick Links
# ----------------------------
with st.sidebar:
    st.header("🔧 Quick Assistance")
    st.write("Common resources:")
    st.markdown("[📖 Product Manuals](https://www.bosch-home.com/service/get-support/instruction-manuals)")
    st.markdown("[🛠️ Service Centers](https://www.bosch-home.com/service/repair)")
    st.markdown("[📦 Warranty Info](https://www.bosch-home.com/service/warranty)")
    st.markdown("[❓ FAQs](https://www.bosch-home.com/service/get-support/faqs)")

    st.divider()
    st.caption("Powered by Azure OpenAI")

# ----------------------------
# 💬 Chat History
# ----------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"]=="user" else "🤖"):
        st.markdown(f"<div class='stChatMessage {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ----------------------------
# 📌 Consumer Enquiry Shortcuts
# ----------------------------
# st.subheader("🛍️ Quick Enquiry Options")
# cols = st.columns(3)
# with cols[0]:
#     if st.button("📦 Track Order"):
#         st.session_state.messages.append({"role": "user", "content": "I want to track my order"})
# with cols[1]:
#     if st.button("⚙️ Product Issue"):
#         st.session_state.messages.append({"role": "user", "content": "I have an issue with my Bosch appliance"})
# with cols[2]:
#     if st.button("💳 Warranty Claim"):
#         st.session_state.messages.append({"role": "user", "content": "I want to claim warranty for my Bosch product"})

# ----------------------------
# 📝 User Input
# ----------------------------
user_input = st.chat_input("Type your question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"<div class='stChatMessage user'>{user_input}</div>", unsafe_allow_html=True)

    # Call Azure Model
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=st.session_state.messages,
        temperature=0.5,
        max_tokens=300
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"<div class='stChatMessage assistant'>{bot_reply}</div>", unsafe_allow_html=True)

# ----------------------------
# 📌 Footer
# ----------------------------
st.markdown("<div class='footer'>Bosch – Invented for life ⚙️</div>", unsafe_allow_html=True)
