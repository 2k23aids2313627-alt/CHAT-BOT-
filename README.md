# 🤖 Mera Private AI Chatbot

Powered by **Claude AI (AWS Bedrock)** + **DuckDuckGo Web Search**

## Features
- 💬 Claude AI se chat karo
- 🔍 Automatic web search (news, latest info ke liye)
- 🔒 Private - sirf tumhare liye
- 🌐 24/7 Online (Streamlit Cloud pe)

## Setup (Streamlit Cloud)

Streamlit Cloud ke **Secrets** mein yeh add karo:

```toml
AWS_ACCESS_KEY_ID = "tumhari_aws_access_key"
AWS_SECRET_ACCESS_KEY = "tumhari_aws_secret_key"
AWS_REGION = "us-east-1"
```

## Local Run karne ke liye

1. `.env` file banao aur keys daalo
2. Install karo:
```bash
pip install -r requirements.txt
```
3. Run karo:
```bash
streamlit run chatbot.py
```
