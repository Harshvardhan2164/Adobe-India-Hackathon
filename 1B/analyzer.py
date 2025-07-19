from sentence_transformers import SentenceTransformer, util

# Load offline model
model = SentenceTransformer("models/all-MiniLM-L6-v2")

def analyze_relevance(chunks, persona, job):
    query = f"{persona} needs to: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["text"], convert_to_tensor=True)
        chunk["score"] = float(util.pytorch_cos_sim(query_embedding, chunk["embedding"]))

    # Sort by score (descending relevance)
    sorted_chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)

    # Annotate importance rank
    for rank, chunk in enumerate(sorted_chunks):
        chunk["importance_rank"] = rank + 1

    return sorted_chunks[:10]  # Top 10 relevant sections
