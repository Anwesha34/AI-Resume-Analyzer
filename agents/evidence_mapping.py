from langchain_core.runnables import RunnableLambda
from sentence_transformers import util

from utils.models import get_embedding_model
from utils.text import split_statements


def extract_key_requirements(jd_text, limit=7):
    statements = split_statements(jd_text)
    if len(statements) <= limit:
        return statements

    model = get_embedding_model()
    statement_embeddings = model.encode(statements, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    scores = util.cos_sim(statement_embeddings, jd_embedding).flatten()
    ranked_indexes = sorted(range(len(statements)), key=lambda index: scores[index].item(), reverse=True)

    return [statements[index] for index in ranked_indexes[:limit]]


def evidence_mapping_agent_fn(state):
    requirements = extract_key_requirements(state.get("jd_text", ""), limit=7)
    resume_chunks = state.get("resume_chunks", [])

    if not requirements or not resume_chunks:
        return {
            "jd_requirements": requirements,
            "evidence_mapping": [
                {"jd_requirement": requirement, "resume_evidence": "", "status": "missing"}
                for requirement in requirements
            ],
        }

    model = get_embedding_model()
    requirement_embeddings = model.encode(requirements, convert_to_tensor=True)
    chunk_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    similarity_matrix = util.cos_sim(requirement_embeddings, chunk_embeddings)

    evidence_mapping = []
    for index, requirement in enumerate(requirements):
        best_index = int(similarity_matrix[index].argmax().item())
        best_score = similarity_matrix[index][best_index].item()
        resume_evidence = resume_chunks[best_index] if best_score >= 0.35 else ""
        evidence_mapping.append({
            "jd_requirement": requirement,
            "resume_evidence": resume_evidence,
            "status": "matched" if resume_evidence else "missing",
        })

    return {
        "jd_requirements": requirements,
        "evidence_mapping": evidence_mapping[:5],
    }


evidence_mapping_agent = RunnableLambda(evidence_mapping_agent_fn)
