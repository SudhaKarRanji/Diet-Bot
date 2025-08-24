# Diet RAG Bot

A Retrieval Augmented Generation (RAG) chatbot specialized in diet and nutrition information using Llama 2 through Ollama.

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed with Llama 3.1
- Git

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Make sure Ollama is running with Llama 3.1 model:
```bash
ollama run llama3.1
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```
2. Open your browser and navigate to the provided URL
3. Start chatting with the bot about diet and nutrition!
