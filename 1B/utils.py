from datetime import datetime

def get_timestamp():
    return datetime.now().isoformat()

def build_output_json(config, sections, timestamp):
    return {
        "metadata": {
            "input_documents": config["documents"],
            "persona": config["persona"],
            "job_to_be_done": config["job_to_be_done"]["task"],
            "processing_timestamp": timestamp
        },
        "extracted_sections": [
            {
                "document": s["document"],
                "page_number": s["page"],
                "importance_rank": s["importance_rank"],
                "section_text": s["text"]
            }
            for s in sections
        ]
    }
