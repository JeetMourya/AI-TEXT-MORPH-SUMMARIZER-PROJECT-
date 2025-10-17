import streamlit as st
import requests

st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📝 AI Text Summarizer & Paraphraser")

API_KEY = "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"

st.success(f"✅ API Key: {API_KEY[:8]}...")

text = st.text_area("Enter text:", height=200)
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                headers = {"Authorization": f"Bearer {API_KEY}"}
                response = requests.post(
                    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
                    headers=headers,
                    json={"inputs": text, "parameters": {"max_length": 150}},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list):
                        st.success("Summary:")
                        st.write(result[0].get('summary_text', 'No summary'))
                else:
                    st.error(f"Error: {response.status_code}")

with col2:
    if st.button("🔄 Paraphrase"):
        if text:
            with st.spinner("Paraphrasing..."):
                headers = {"Authorization": f"Bearer {API_KEY}"}
                # Using a working model for text generation
                response = requests.post(
                    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                    headers=headers,
                    json={"inputs": f"Rephrase this: {text}", "parameters": {"max_length": 200}},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Paraphrased:")
                    st.write(result[0].get('generated_text', 'Try again'))
                else:
                    st.error(f"Paraphrase Error: {response.status_code}")
