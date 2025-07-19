import json
from processor import extract_text_chunks
from analyzer import analyze_relevance
from utils import get_timestamp, build_output_json

if __name__ == "__main__":
    with open("challenge1b_input.json", "r") as f:
        config = json.load(f)

    all_chunks = extract_text_chunks(config["documents"])
    ranked_sections = analyze_relevance(
        all_chunks, config["persona"]["role"], config["job_to_be_done"]["task"]
    )

    final_output = build_output_json(
        config, ranked_sections, get_timestamp()
    )

    with open("output.json", "w") as f:
        json.dump(final_output, f, indent=4)

    print("✅ Done. Output saved to output.json")
