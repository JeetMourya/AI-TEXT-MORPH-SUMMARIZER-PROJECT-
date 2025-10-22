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
    
