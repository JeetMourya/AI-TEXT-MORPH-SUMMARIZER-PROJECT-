# AI Text Morph Summarizer Project

🚀 **An advanced AI-powered text summarization and paraphrasing tool** that combines extractive and abstractive summarization with intelligent paraphrasing capabilities.

---

## 📋 Project Overview

This project provides a comprehensive solution for text processing with three main functionalities:
- **🧠 Abstractive Summarization** - Generates new sentences that capture the essence of original text
- **📄 Extractive Summarization** - Selects and extracts important sentences from original text  
- **✨ Intelligent Paraphrasing** - Rewrites text while preserving meaning using advanced LLMs

---

## 🛠️ Technical Architecture

### Core Components

| Module | Technology Used | Purpose |
|--------|-----------------|---------|
| **Abstractive Summarizer** | Hugging Face BART-large-CNN | Generates human-like summaries |
| **Extractive Summarizer** | Hugging Face BART-large-CNN | Extracts key sentences |
| **Paraphraser** | Groq API + LLaMA 3.1 | Rewrites text naturally |
| **Pipeline** | Custom Python Class | Orchestrates all modules |

### API Integrations
- **🤗 Hugging Face Inference API** - For summarization tasks
- **⚡ Groq Cloud API** - For high-speed paraphrasing
- **🔐 Environment Variables** - Secure credential management

---
```
## 📁 Project Structure
AI-TEXT-MORPH-PROJECT/
├── mvp/
│ ├── init.py
│ ├── abstractive.py # Abstractive summarization
│ ├── extractive.py # Extractive summarization
│ ├── parapharsing.py # Text paraphrasing
│ ├── mvp_pipeline.py # Main pipeline
│ └── test_run.py # Test scripts
├── simple_app.py # Simple CLI application
├── ui_app.py # Streamlit web interface
├── requirements.txt # Dependencies
├── config.yaml # Configuration
├── .env.example # Environment template
└── README.md # This file
```


---

## ⚡ Quick Start
### Prerequisites
```
- Python 3.8+
- Hugging Face API Key
- Groq API Key (optional, for paraphrasing)
```
## Installation
```

1. **Clone the repository**
```bash
git clone https://github.com/JeetMourya/AI-TEXT-MORPH-SUMMARIZER-PROJECT-.git
cd AI-TEXT-MORPH-SUMMARIZER-PROJECT-
Install dependencies

bash
pip install -r requirements.txt
Setup environment variables

bash
cp .env.example .env
# Add your API keys to .env file
Run the application

bash
# Streamlit UI
streamlit run ui_app.py

# Or simple CLI
python simple_app.py
🎯 Usage Examples
Abstractive Summarization
python
from mvp.abstractive import AbstractiveSummarizer

summarizer = AbstractiveSummarizer(api_key="your_hf_key")
summary = summarizer.summarize(text, length='medium')
Extractive Summarization
python
from mvp.extractive import ExtractiveSummarizer

summarizer = ExtractiveSummarizer(api_key="your_hf_key")
summary = summarizer.summarize(text, length='short')
Paraphrasing
python
from mvp.parapharsing import Paraphraser

paraphraser = Paraphraser()
variations = paraphraser.paraphrase(text, num_return_sequences=3)
Complete Pipeline
python
from mvp.mvp_pipeline import SummarizationPipeline

pipeline = SummarizationPipeline(hf_api_key="your_key")
abstractive = pipeline.summarize(text, method="abstractive")
paraphrased = pipeline.paraphrase("Sample text", 2)

```
##🔧 Configuration
```
Update config.yaml for customization:

yaml
summarization:
  max_length: 200
  min_length: 30
  temperature: 0.7

paraphrasing:
  model: "llama-3.1-8b-instant"
  max_tokens: 400
📊 Features
✅ Dual Summarization Approaches - Abstractive & Extractive
✅ Intelligent Paraphrasing - Multiple variations
✅ REST API Integration - Hugging Face + Groq APIs
✅ Web Interface - Streamlit-based UI
✅ Modular Architecture - Easy to extend
✅ Error Handling - Robust API communication
✅ Security - Environment-based credential management
```
## 🚀 Performance
Fast Inference via Groq's accelerated computing

High Quality using state-of-the-art models (BART, LLaMA 3.1)

Scalable cloud-based API architecture

Flexible configurable output lengths
```

## 👨‍💻 Developer
```
Developed by: Jeet Mourya
💡 AI Enthusiast & Full-Stack Developer
🔗 GitHub Profile

Contribution
Feel free to contribute to this project by:

Reporting bugs

Suggesting new features

Submitting pull requests

Improving documentation
```

## 📄 License
```
This project is open source and available under the MIT License.

🤝 Support
For support, email or create an issue in the repository.

⭐ If you find this project useful, please give it a star on GitHub!

```
