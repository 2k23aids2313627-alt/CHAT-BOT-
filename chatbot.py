import streamlit as st
import boto3
from duckduckgo_search import DDGS

# =====================
# AWS Configuration
# =====================
AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = st.secrets["AWS_REGION"]

MODEL_ID = "us.anthropic.claude-sonnet-4-5"

# AWS Bedrock Client
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# =====================
# Web Search Function
# =====================
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                search_text = ""
                for r in results:
                    search_text += f"• {r['title']}: {r['body']}\n"
                return search_text
    except Exception as e:
        return f"Search not available: {str(e)}"

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="JARVIS",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 JARVIS")
st.caption("Powered by Claude (AWS Bedrock) + DuckDuckGo Web Search")

# =====================
# Chat History
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.divider()

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# =====================
# User Input
# =====================
if prompt := st.chat_input("Kuch bhi pucho..."):

    # Keywords jinpe search hoga automatically
    search_keywords = [
        "latest", "news", "today", "current", "abhi", "aaj",
        "kya hua", "recent", "2024", "2025", "2026", "price",
        "result", "score", "weather", "mausam"
    ]
    needs_search = any(kw in prompt.lower() for kw in search_keywords)

    # Web search if needed
    search_context = ""
    if needs_search:
        with st.spinner("🔍 Web search ho rahi hai..."):
            search_context = web_search(prompt)

    # Full prompt with search context
    full_prompt = prompt
    if search_context:
        full_prompt = f"""User ka question: {prompt}

Web search results:
{search_context}

Inke basis pe jawab do."""

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    st.chat_message("user").write(prompt)

    # Call Claude via AWS Bedrock
    with st.spinner("🤔 Claude soch raha hai..."):
        try:
            api_messages = []
            for m in st.session_state.messages[:-1]:
                api_messages.append({
                    "role": m["role"],
                    "content": [{"text": m["content"]}]
                })
            api_messages.append({
                "role": "user",
                "content": [{"text": full_prompt}]
            })

            response = client.converse(
                modelId=MODEL_ID,
                messages=api_messages,
                inferenceConfig={"maxTokens": 1000}
            )

            reply = response['output']['message']['content'][0]['text']

        except Exception as e:
            reply = f"❌ Error aaya: {str(e)}"

    # Show reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    st.chat_message("assistant").write(reply)
