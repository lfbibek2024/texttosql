# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose Streamlit port
EXPOSE 8501

# Initialize SQLite DB and ChromaDB if not exists, then run Streamlit
ENTRYPOINT ["/bin/bash", "-c", "if [ ! -f leafpay.db ]; then sqlite3 leafpay.db < leafpay.db_init.sql; fi && python retriever/init_leafpay_chromadb.py && streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"]
