# Intelligent Document Analyst (Round 1B - Adobe Hackathon)

## Overview

This project is part of the **Adobe India Hackathon – Connecting the Dots Challenge (Round 1B)**.  
It analyzes a **set of documents** to extract the most relevant **sections and sub-sections** based on a specific **persona** and **job-to-be-done**, returning a structured **JSON output** with ranked segments and refined text snippets.

The system runs **fully offline**, uses a **lightweight SentenceTransformer model** (`all-MiniLM-L6-v2`, <1GB), and processes 3–5 documents within **60 seconds** on **CPU-only machines**.

## Features

- **Metadata Extraction**  
  Captures persona, job-to-be-done, document names, and processing timestamp.

- **Relevant Section Extraction**  
  Identifies top-ranked sections across multiple PDF documents using **semantic similarity** with `sentence-transformers`.

- **Sub-section Refinement**  
  Within each relevant section, finds key sentences or sub-points aligned with the user’s objective.

- **Fully Offline & Fast**  
  No internet or cloud APIs required.  
  Processes PDFs quickly using **PyMuPDF** and **preloaded SentenceTransformer** models.

- **Dockerized for Easy Deployment**  
  Easily run in isolated environments using Docker (CPU-only, <1GB RAM usage).

## Output Format

Each run produces an `output.json` file like this:

```json
{
  "metadata": {
    "input_documents": [{ "filename": "South of France - Cuisine.pdf", "title": "South of France - Cuisine" }],
    "persona": { "role": "Travel Planner" },
    "job_to_be_done": { "task": "Plan a trip of 4 days for a group of 10 college friends." },
    "processing_timestamp": "2025-07-18T12:34:56"
  },
  "extracted_sections": [
    {
      "document": "South of France - Things to Do.pdf",
      "page_number": 2,
      "section_title": "Outdoor Adventures in Provence",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "document": "South of France - Things to Do.pdf",
      "page_number": 2,
      "refined_text": [
        "Hike the Calanques for stunning sea cliffs and turquoise waters.",
        "Rent bikes to explore the lavender fields in Valensole.",
        "Take a hot air balloon ride over vineyards near Avignon."
      ]
    }
  ]
}
```

## Tech Stack

- **Python 3.10**
- **PyMuPDF** – Extract text and layout from PDFs
- **SentenceTransformers** – Semantic similarity using `all-MiniLM-L6-v2`
- **Docker** – For containerized, reproducible CPU-only runs

## Installation and Usage

### 1. Local Testing (Without Docker)

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Required files

- `main.py` – Main script
- `challenge1b_input.json` – Contains persona, task, and list of PDFs
- `documents/` – Folder with all PDF files
- `models/all-MiniLM-L6-v2/` – Pre-downloaded model directory

#### Run

```bash
python main.py
```

> Output is saved to `output.json` in the current directory.

### 2. Dockerized Usage

#### Build the Docker image

```bash
docker build -t intelligent-doc-analyzer .
```

#### Run the container

```bash
docker run --rm \
-v "$PWD:/app" \
--network none \
intelligent-doc-analyzer
```

## Constraints & Performance

- **Offline only** – No internet required
- **CPU-only** – No GPU or CUDA dependencies
- **≤ 1GB RAM** – Lightweight model (`all-MiniLM-L6-v2`)
- **Fast** – Analyzes 3–5 documents within **60 seconds**
- **Secure** – No external API calls or data leakage

## Folder Structure

```
.
├── main.py
├── challenge1b_input.json
├── output.json (generated)
├── documents/
│   └── *.pdf
├── models/
│   └── all-MiniLM-L6-v2/
├── Dockerfile
└── requirements.txt
```

## Acknowledgments

This project was built as part of **Adobe India Hackathon 2025**, showcasing document intelligence capabilities using open-source tools and language models.
