import streamlit as st
import requests

st.set_page_config(
    page_title="Text Summarization using Mistral AI",
    page_icon="📝"
)

st.title("📝 Text Summarization using Mistral AI")
st.write("Enter a long paragraph and generate a short, simple summary.")

API_KEY = "mstrl_2exDtrhHd8MkRAERkXM0oaaJdsVJ0zOp_13TiEz"

text = st.text_area(
    "Enter your paragraph:",
    placeholder="Paste your long paragraph here...",
    height=250
)

def simple_summary(text):
    sentences = text.replace("!", ".").replace("?", ".").split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 2:
        return text.strip()

    return ". ".join(sentences[:2]) + "."

if st.button("Summarize"):

    if not text.strip():
        st.warning("Please enter a paragraph first.")

    else:
        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Summarize this paragraph in simple English. "
                        "Keep only the important points:\n\n" + text
                    )
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                summary = result["choices"][0]["message"]["content"]

            else:
                # Fallback summary if Mistral rate limit is reached
                summary = simple_summary(text)

            st.subheader("Generated Summary")
            st.success(summary)

        except Exception:
            summary = simple_summary(text)

            st.subheader("Generated Summary")
            st.success(summary)