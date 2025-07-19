import os
import fitz  # PyMuPDF

def extract_text_chunks(documents):
    chunks = []
    for doc in documents:
        filename = doc["filename"]
        doc_path = os.path.join("documents", filename)  # Add the folder name here

        if not os.path.exists(doc_path):
            print(f"❌ File not found: {doc_path}")
            continue  # or raise an error

        doc_fitz = fitz.open(doc_path)
        for page_num in range(len(doc_fitz)):
            page = doc_fitz.load_page(page_num)
            text = page.get_text()
            if text.strip():
                chunks.append({
                    "document": filename,
                    "page": page_num + 1,
                    "text": text
                })
    return chunks
