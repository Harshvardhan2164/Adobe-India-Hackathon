import os
import fitz
import json
import datetime
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

DOCUMENT_FOLDER = "documents"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K_SECTIONS = 1
TOP_K_SUBSECTIONS = 3
MAX_PAGES = 5

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open("challenge1b_input.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)

PERSONA = input_data["persona"]["role"]
JOB_TO_BE_DONE = input_data["job_to_be_done"]["task"]

DOCUMENT_LIST = [doc["filename"] for doc in input_data["documents"]]

def load_pdfs(folder, doc_list):
    documents = []
    for filename in doc_list:
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            doc = fitz.open(path)
            documents.append((filename, doc))
        else:
            print(f"⚠️ File not found: {filename}")
    return documents

def split_into_sections(doc, filename):
    sections = []
    for page_num in range(min(len(doc), MAX_PAGES)):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text) > 100:
                sections.append({
                    "document": filename,
                    "page_number": page_num + 1,
                    "text": text
                })
    return sections

def semantic_ranking(sections, query, top_k):
    section_texts = [s['text'] for s in sections]
    if not section_texts:
        return []
    section_embeddings = model.encode(section_texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, section_embeddings)[0]
    top_indices = scores.argsort(descending=True)[:top_k]
    return [sections[i] for i in top_indices]

def analyze_documents():
    all_docs = load_pdfs(DOCUMENT_FOLDER, DOCUMENT_LIST)
    timestamp = datetime.datetime.now().isoformat()

    metadata = {
        "input_documents": [{"filename": name, "title": name.replace('.pdf', '')} for name, _ in all_docs],
        "persona": {"role": PERSONA},
        "job_to_be_done": {"task": JOB_TO_BE_DONE},
        "processing_timestamp": timestamp
    }

    all_sections = []
    for filename, doc in tqdm(all_docs, desc="Processing PDFs"):
        sections = split_into_sections(doc, filename)
        top_sections = semantic_ranking(sections, JOB_TO_BE_DONE, TOP_K_SECTIONS)
        for rank, section in enumerate(top_sections):
            section["section_title"] = section["text"].split("\n")[0][:50]
            section["importance_rank"] = rank + 1
            all_sections.append(section)

    extracted_sections_json = [
        {
            "document": s["document"],
            "page_number": s["page_number"],
            "section_title": s["section_title"],
            "importance_rank": s["importance_rank"]
        }
        for s in all_sections
    ]

    sub_section_analysis_json = []
    for section in all_sections:
        lines = section["text"].split("\n")
        sub_candidates = [line.strip() for line in lines if len(line.strip()) > 30]
        sub_scores = semantic_ranking(
            [{"text": text, "document": section["document"], "page_number": section["page_number"]} for text in sub_candidates],
            JOB_TO_BE_DONE,
            TOP_K_SUBSECTIONS
        )
        sub_section_analysis_json.append({
            "document": section["document"],
            "page_number": section["page_number"],
            "refined_text": [s["text"] for s in sub_scores]
        })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections_json,
        "sub_section_analysis": sub_section_analysis_json
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n Output saved to output.json")

if __name__ == "__main__":
    analyze_documents()