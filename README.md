# Generative AI Text-to-SQL System

## Overview
This project enables users to interact with databases using natural language, converting questions into SQL queries using a RAG architecture with LangChain, OpenAI GPT-4, ChromaDB/Pinecone, and LangSmith. A Streamlit web interface is provided for ease of use.

## Features
- Natural language to SQL conversion
- Retrieval-augmented generation (RAG)
- Schema and example query retrieval
- Prompt engineering for accuracy
- SQL validation
- LangSmith observability
- Streamlit web UI

## Setup
1. Copy `.env.example` to `.env` and fill in your API keys.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run frontend/app.py`

## Structure
- `app/` - Orchestration logic
- `retriever/` - Schema & example query retrieval
- `generator/` - Prompting & LLM logic
- `validator/` - SQL validation
- `frontend/` - Streamlit UI
