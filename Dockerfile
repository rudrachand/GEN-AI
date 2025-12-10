FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
COPY langgraph_rag.py /app/
COPY app.py /app/
COPY ui.py /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

CMD ["sh", "-c", "\
uvicorn app:app --host 0.0.0.0 --port 8000 & \
echo 'Waiting for FastAPI to start...' && \
until curl -s http://localhost:8000/docs > /dev/null; do \
    echo 'FastAPI not ready, waiting...'; \
    sleep 1; \
done; \
echo 'FastAPI started. Launching Streamlit...' && \
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0 \
"]
