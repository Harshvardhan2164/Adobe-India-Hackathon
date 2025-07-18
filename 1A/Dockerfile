FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pymupdf

COPY outline_extractor.py .

CMD ["python", "outline_extractor.py"]