# 🌐 Web Summarizer

**Live app:** https://website-summarizer-ollama-builds-unique.streamlit.app

An AI-powered web summarizer built with Streamlit and Groq API.  
Paste any URL and get an instant markdown summary powered by Llama 3.1.

## Features

- Scrapes any public website
- Summarizes content using Llama 3.1 8B (via Groq — free & fast)
- Clean markdown output
- No backend required — runs entirely in Streamlit

## Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Enter your free [Groq API key](https://console.groq.com) in the sidebar.

## Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository (make sure `app.py` and `requirements.txt` are at the root)

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub

3. Click **"New app"** and select your repo, branch, and set the main file to `app.py`

4. Click **Deploy** — your app will be live at `https://yourname-appname.streamlit.app`

> **Note:** Users enter their own Groq API key in the sidebar, so no secrets need to be configured on Streamlit Cloud.  
> If you want to provide a shared key instead, add it under **App settings → Secrets**:
>
> ```toml
> GROQ_API_KEY = "gsk_your_key_here"
> ```

## Get a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Navigate to **API Keys** and create a new key
4. Paste it into the sidebar when running the app
