import json
import os
import re
import fitz
import unicodedata

def normalize_text(text):
    return unicodedata.normalize("NFKC", text).strip()

def check_bold_italic(font_name):
    font_name_lower = font_name.lower()
    return ("bold" in font_name_lower) or ("italic" in font_name_lower)

def extract_pdf_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = []

    # Step 1: Collect text blocks with font size
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue
                
            for line in block["lines"]:
                line_text = ""
                max_font_size = 0
                bold_found = False

                for span in line["spans"]:
                    raw_text = span["text"].strip()

                    if not raw_text:
                        continue
                    
                    clean_text = normalize_text(raw_text)
                    line_text += clean_text + " "
                    
                    max_font_size = max(max_font_size, span["size"])

                    if check_bold_italic(span["font"]):
                        bold_found = True
                
                line_text = re.sub(r"\s+", " ", line_text).strip()

                if line_text:
                    headings.append({
                        "text": line_text,
                        "page": page_num+1,
                        "font_size": max_font_size,
                        "bold": bold_found
                    })
                    
                    font_sizes.append(max_font_size)
                    
    # Step 2: Determine font size thresholds
    unique_sizes = sorted(list(set(font_sizes)), reverse=True)

    if len(unique_sizes) >= 3:
        title_size, h1_size, h2_size = unique_sizes[:3]
    
    else:
        title_size = unique_sizes[0]
        h1_size = unique_sizes[0] * 0.9
        h2_size = unique_sizes[0] * 0.8
        
    # Step 3: Identify title
    title_candidates = [
        h for h in headings if h["page"] == 1 and (h["font_size"] >= title_size or h["bold"])
    ]
    
    title_candidates = sorted(title_candidates, key=lambda x: (-x["font_size"], x["text"]))
    title = title_candidates[0]["text"] if title_candidates else "Untitled Document"

    # Step 4: Classify headings H1/H2/H3
    outline = []

    for h in headings:
        level = None
        
        if h["font_size"] >= title_size * 0.95:
            level = "H1"
        elif h["font_size"] >= h1_size * 0.95:
            level = "H2"
        elif h["font_size"] >= h2_size * 0.95:
            level = "H3"
            
        if h["bold"] and level is None:
            level = "H3"

        if (level or h["bold"]) and len(h["text"].split()) < 15:
            outline.append({
                "level": level if level else "H3",
                "text": h["text"],
                "page": h["page"]
            })
    
    return {
        "title": title,
        "outline": outline
    }
    
def process_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            output_json = extract_pdf_outline(pdf_path)
            
            json_file = file.replace(".pdf", ".json")
            json_path = os.path.join(output_dir, json_file)
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output_json, f, indent=2, ensure_ascii=False)
                
if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    process_pdfs(input_dir, output_dir)
    