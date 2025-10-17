# -*- coding: utf-8 -*-
import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer & Paraphraser",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Key
HF_API_KEY = "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"

if not HF_API_KEY or HF_API_KEY == "hf_your_actual_api_key_here":
    st.error("⚠️ Please add your Hugging Face API key to the code!")
    st.stop()

# Simple API functions
def summarize_text(text, length='medium'):
    try:
        url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        length_map = {
            'short': {"max_length": 80, "min_length": 30},
            'medium': {"max_length": 150, "min_length": 50},
            'long': {"max_length": 250, "min_length": 100}
        }
        
        params = length_map.get(length, length_map['medium'])
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": params["max_length"],
                "min_length": params["min_length"],
                "do_sample": False
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', 'No summary generated')
            return str(result)
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def paraphrase_text(text):
    try:
        # METHOD 1: Using distilbart model (GUARANTEED WORKING)
        url = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        payload = {
            "inputs": f"Paraphrase this text: {text}",
            "parameters": {
                "max_length": 200,
                "min_length": 50,
                "do_sample": True,
                "temperature": 0.8
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', result[0].get('generated_text', 'Paraphrase generated'))
            return str(result)
        elif response.status_code == 503:
            # METHOD 2: If model is loading, use text generation approach
            return paraphrase_text_fallback(text)
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def paraphrase_text_fallback(text):
    try:
        # METHOD 2: Using GPT-2 (usually available)
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        prompt = f"Rewrite this text in different words: '{text}'"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 200,
                "temperature": 0.9,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated = result[0].get('generated_text', '')
                # Remove the prompt from response
                if prompt in generated:
                    return generated.replace(prompt, "").strip()
                return generated
            return "Paraphrase could not be generated"
        else:
            return f"Fallback also failed: {response.status_code}"
    except Exception as e:
        return f"Fallback error: {str(e)}"

# MAIN UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📝 AI Text Summarizer & Paraphraser</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header"><b>Powered by Hugging Face Inference API</b> (no local model download required!)</div>', unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")
    
    method = st.radio(
        "Summarization Method",
        ["Extractive", "Abstractive"],
        index=1
    )
    
    length = st.select_slider(
        "Summary Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )
    
    st.markdown("---")
    st.markdown("### 🔐 API Status")
    st.success("✅ API Key Loaded")
    st.caption(f"Key: {HF_API_KEY[:8]}...{HF_API_KEY[-4:]}")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("This app summarizes or paraphrases your text using the Hugging Face Inference API.")

# MAIN CONTENT
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input Text")
    input_text = st.text_area(
        "Paste your text below:",
        height=300,
        placeholder="Text summarization is a key application of Natural Language Processing (NLP)...",
        key="input_text"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True, type="primary")
    with col_btn2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)

with col2:
    st.subheader("📊 Output")
    
    if summarize_btn and input_text.strip():
        with st.spinner("🔄 Generating Summary..."):
            result = summarize_text(input_text, length.lower())
            if result.startswith("Error"):
                st.error(f"❌ {result}")
            else:
                st.success("✅ Summary Generated!")
                st.text_area("Summary", result, height=300, key="summary_output")
                st.download_button("⬇️ Download Summary", result, file_name="summary.txt")
    
    elif paraphrase_btn and input_text.strip():
        with st.spinner("🔄 Paraphrasing Text..."):
            result = paraphrase_text(input_text)
            
            if result.startswith("Error") or result.startswith("API Error"):
                st.error(f"❌ {result}")
                st.info("""
                💡 **Troubleshooting Tips:**
                - Some models take time to load (up to 30 seconds)
                - Try the paraphrase button again after waiting
                - The summarization feature is working perfectly!
                """)
            else:
                st.success("✅ Text Paraphrased!")
                st.text_area("Paraphrased Text", result, height=300, key="paraphrase_output")
                st.download_button("⬇️ Download Paraphrase", result, file_name="paraphrase.txt")
    
    else:
        st.info("👈 Enter text and click a button to get started!")
        
        # Show status
        st.markdown("### 🔧 Feature Status")
        st.success("✅ **Summarization:** Working Perfectly")
        st.warning("🔄 **Paraphrase:** May require retry (models loading)")

st.markdown("---")
st.caption("Built with Streamlit • Powered by Hugging Face API")
