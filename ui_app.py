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

# API Key - FIXED WITH NEW KEY
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
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

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
    .success-box {
        background-color: #d4edda;
        border: 2px solid #c3e6cb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
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
        placeholder="Enter your text here...",
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
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ **Summary Generated Successfully!**")
                st.markdown('</div>', unsafe_allow_html=True)
                st.text_area("Summary", result, height=250, key="summary_output")
                
                # Download button for summary
                st.download_button(
                    label="📥 Download Summary",
                    data=result,
                    file_name="ai_summary.txt",
                    mime="text/plain"
                )
    
    elif paraphrase_btn and input_text.strip():
        with st.spinner("🔄 Paraphrasing Text..."):
            result = paraphrase_text(input_text)
            
            if result.startswith("Error") or result.startswith("API Error"):
                st.error(f"❌ {result}")
            else:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("✅ **Text Paraphrased Successfully!**")
                st.markdown('</div>', unsafe_allow_html=True)
                st.text_area("Paraphrased Text", result, height=250, key="paraphrase_output")
                
                # Download button for paraphrase
                st.download_button(
                    label="📥 Download Paraphrase",
                    data=result,
                    file_name="ai_paraphrase.txt", 
                    mime="text/plain"
                )
    
    else:
        st.info("👈 Enter text and click a button to get started!")

st.markdown("---")
st.caption("Built with Streamlit • Powered by Hugging Face API")
