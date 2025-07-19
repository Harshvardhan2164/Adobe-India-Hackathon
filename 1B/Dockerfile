FROM --platform=linux/amd64 python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     poppler-utils \
#     libglib2.0-0 \
#     libxrender1 \
#     libsm6 \
#     libxext6 \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
COPY models/all-MiniLM-L6-v2 /app/models/all-MiniLM-L6-v2

COPY . .

CMD ["python", "main.py"]
