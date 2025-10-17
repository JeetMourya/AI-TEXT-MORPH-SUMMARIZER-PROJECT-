from setuptools import setup, find_packages

setup(
    name="ai-text-morph-project",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
    ],
    author="Thangarasu",
    author_email="thangamani1128@gmail.com",
    description="AI Text Summarizer and Paraphraser using Hugging Face API",
    python_requires=">=3.8",
    include_package_data=True,
)