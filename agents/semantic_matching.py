from langchain_core.runnables import RunnableLambda
from sentence_transformers import util

from utils.models import get_embedding_model


def _weighted_average(scores):
    weights = [1.0, 0.85, 0.7, 0.55, 0.4]
    selected_weights = weights[:len(scores)]
    return sum(score * weight for score, weight in zip(scores, selected_weights)) / sum(selected_weights)


def select_relevant_chunks(chunks, jd_text, top_k=5):
    if not chunks or not jd_text:
        return [], 0.0

    model = get_embedding_model()
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    scores = util.cos_sim(chunk_embeddings, jd_embedding).flatten()
    ranked = sorted(
        [
            {"resume_chunk": chunk, "score": max(0.0, score.item())}
            for chunk, score in zip(chunks, scores)
        ],
        key=lambda item: item["score"],
        reverse=True,
    )
    top_matches = ranked[:5]
    semantic_score = _weighted_average([item["score"] for item in top_matches]) * 100 if top_matches else 0.0

    return top_matches[:top_k], round(max(0.0, min(semantic_score, 100.0)), 2)


def semantic_matching_agent_fn(state):
    top_matches, semantic_score = select_relevant_chunks(
        state.get("resume_chunks", []),
        state.get("jd_text", ""),
        top_k=5,
    )

    return {
        "semantic_matches": top_matches,
        "relevant_resume_chunks": [item["resume_chunk"] for item in top_matches],
        "semantic_score": semantic_score,
    }


semantic_matching_agent = RunnableLambda(semantic_matching_agent_fn)
