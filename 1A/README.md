# Structured PDF Outline Extractor (Round 1A - Adobe Hackathon)

## Overview

This project is part of **Adobe India Hackathon – Connecting the Dots Challenge (Round 1A)**.  
It extracts a **structured outline** from a PDF document by detecting the **Title, H1, H2, and H3 headings**, along with their **page numbers**, and outputs them in a **clean JSON format**.

Unlike traditional PDF readers, this tool **understands document structure** using **font size, bold/italic style, and text heuristics**. It also supports **multilingual text** (UTF-8).

## Features

- **Title Detection**  
  Finds the most prominent heading on the first page.  

- **Heading Classification**  
  Detects and classifies headings into **H1, H2, H3** using:
  - **Font size hierarchy**
  - **Bold/italic style detection**
  - **Short-line heuristic** (headings are usually short)

- **Multilingual Support**  
  Preserves non-English characters (e.g., Japanese, Chinese, Arabic) in JSON output.  

- **Fast & Offline**  
  Runs fully offline with **PyMuPDF**, no internet calls needed.  
  Processes a **50-page PDF in ≤10 seconds**.

- **Dockerized for easy deployment**  
  Works on **CPU-only (amd64)** systems.

## Output Format

Each PDF generates a JSON with the following structure:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Tech Stack

* **Python** 3.10
* **PyMuPDF** for:
    * Extracting text
    * Detecting font size and style
* **Docker** for containerization

## Installation and Usage

### 1. Local Testing without Docker

1. Install Python dependencies

    ```bash
    pip install pymupdf
    ```

2. Run the script

    ```bash
    python outline_extractor.py
    ```

3. Check the output

    Each `file.path` in `input/` generates `file.json` in `output/`

### 2. Running with Docker

1. Build Docker image

    ```bash
    docker build --platform linux/amd64 -t pdf-outline-extractor .
    ```

2. Run container

    ```bash
    docker run --rm \
    -v //c/path/to/project/input:/app/input \
    -v //c/path/to/project/output:/app/output \
    --network none pdf-outline-extractor
    ```

    Windows users: Replace C:\ paths with //c/ style paths for Docker compatibility.

    ```powershell
    docker run --rm ^
    -v //c/Users/YourName/Desktop/input:/app/input ^
    -v //c/Users/YourName/Desktop/output:/app/output ^
    --network none pdf-outline-extractor
    ```

3. Results

    PDFs from `input/` → JSONs in `outputs/`

### Working

1. Extract text blocks
    For each line, we extract:
        * Text
        * Font size
        * Font style (bold/italic)

2. Analyze font hierarchy
    * Largest font on page 1 → Title
    * Next levels → H1, H2, H3

3. Heading heuristics
    * Bold or italic text → higher heading likelihood
    * Very short lines (≤10 words) → more likely a heading

4. Multilingual normalization
    * Unicode normalized to support multiple languages.
    * JSON saved with `ensure_ascii=False` for readable output.

## Performance & Constraints

* Processes a 50-page PDF in ≤10 seconds
* Works offline (no API calls)
* Runs on CPU only (amd64)
* No heavy ML model (>200MB)