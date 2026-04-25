import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# --- Page config ---
st.set_page_config(
    page_title="Web Summarizer",
    page_icon="🌐",
    layout="centered"
)

# --- Scraper ---
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

def scrape_website(url: str) -> dict:
    """Scrape title and text content from a URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string.strip() if soup.title else "No title found"

    # Remove noise
    for tag in soup.body(["script", "style", "img", "input", "nav", "footer"]):
        tag.decompose()

    text = soup.body.get_text(separator="\n", strip=True) if soup.body else ""

    # Limit to avoid token overload
    text = text[:4000]

    return {"title": title, "text": text}


def summarize(title: str, text: str, api_key: str) -> str:
    """Send scraped content to Groq and return a markdown summary."""
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an assistant that analyzes the contents of a website "
        "and provides a clear, concise summary. "
        "Ignore navigation-related text. "
        "Respond in markdown."
    )

    user_prompt = (
        f"You are looking at a website titled: **{title}**\n\n"
        "The contents of this website are as follows. "
        "Please provide a short summary in markdown. "
        "If it includes news or announcements, summarize those too.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


# --- UI ---
st.title("🌐 Web Summarizer")
st.markdown("Paste any URL and get an instant AI-powered summary.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at https://console.groq.com"
    )
    st.markdown("---")
    st.markdown("**Model:** Llama 3.1 8B (via Groq)")
    st.markdown("**Free tier:** ✅ Yes")
    st.markdown("[Get your free Groq API key →](https://console.groq.com)")

# Main input
url = st.text_input(
    "Enter a URL",
    placeholder="https://en.wikipedia.org/wiki/Python_(programming_language)",
)

if st.button("Summarize", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Scraping website..."):
            result = scrape_website(url)

        if "error" in result:
            st.error(f"Failed to fetch the website: {result['error']}")
        else:
            with st.spinner("Summarizing with AI..."):
                try:
                    summary = summarize(result["title"], result["text"], api_key)
                    st.success("Done!")
                    st.markdown(f"### 📄 {result['title']}")
                    st.markdown("---")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Error from Groq API: {e}")
