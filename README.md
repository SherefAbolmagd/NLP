# Dr. X Publications Analysis System

A NLP-powered system to analyze Dr. X's research publications with RAG capabilities, translation, and summarization tools.

## Features

- 📄 Multi-format document processing (PDF, DOCX, CSV, Excel)
- 🔍 Semantic search with hybrid retrieval (vector + keyword)
- 💬 Question answering with local LLM (Mistral-7B)
- 🌍 Translation to English/Arabic
- ✂️ Text summarization with quality evaluation
- 📊 Performance monitoring

## Prerequisites

- Python 3.8+
- 8GB+ RAM (16GB recommended for larger documents)
- 10GB+ free disk space (for models and database)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/dr_x_analysis.git
cd dr_x_analysis
```

### 2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Mistral-7B (4.36GB)
```bash
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```