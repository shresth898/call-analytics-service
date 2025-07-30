from sentence_transformers import SentenceTransformer
from app.utils.nlp_helpers import cosine_similarity
from typing import List
from app.db.models import Call

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()

def get_similar_calls(reference_call: Call, all_calls: List[Call], top_k: int = 5) -> List[str]:
    if reference_call.embedding is None:
        return []

    similarities = []

    for call in all_calls:
        if call.call_id == reference_call.call_id or not call.embedding:
            continue
        sim = cosine_similarity(reference_call.embedding, call.embedding)
        similarities.append((call.call_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [call_id for call_id, _ in similarities[:top_k]]
