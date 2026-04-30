from langchain_core.runnables import RunnableLambda
from sentence_transformers import util

from llm.client import invoke_structured
from llm.schemas import ReasoningOutput
from utils.models import get_embedding_model


def _match_skills(resume_skills, jd_skills):
    if not jd_skills:
        return [], []

    if not resume_skills:
        return [], jd_skills

    model = get_embedding_model()
    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)
    scores = util.cos_sim(jd_embeddings, resume_embeddings)

    matched = []
    missing = []
    for index, skill in enumerate(jd_skills):
        if scores[index].max().item() >= 0.72:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


def _reason_with_llm(state, matched_skills, missing_skills):
    template = """
Validate fit and produce concise recruiter output. Use only provided context. No invented evidence.

Relevant resume context:
{resume_context}

JD requirements:
{jd_requirements}

Extracted skills:
{extracted_skills}

Matched:
{matched_skills}

Missing:
{missing_skills}

Evidence:
{evidence_mapping}

Semantic score: {semantic_score}

{format_instructions}
"""
    resume_context = "\n".join(state.get("relevant_resume_chunks", [])[:5])
    jd_requirements = "\n".join(state.get("jd_requirements", [])[:7])
    return invoke_structured(
        ReasoningOutput,
        template,
        fallback=ReasoningOutput(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            improvement_actions=[
                "Add clearer evidence for the most important job requirements.",
                "Quantify technical impact and project outcomes.",
            ],
            summary="The resume has some relevant overlap with the job description.\nReview missing skills and strengthen direct evidence for the role.",
            llm_score=state.get("semantic_score", 0.0),
        ),
        resume_context=resume_context,
        jd_requirements=jd_requirements,
        extracted_skills=state.get("extracted_skills", {}),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        evidence_mapping=state.get("evidence_mapping", [])[:5],
        semantic_score=state.get("semantic_score", 0.0),
    )


def llm_reasoning_agent_fn(state):
    skills = state.get("extracted_skills", {})
    matched_skills, missing_skills = _match_skills(
        skills.get("resume", []),
        skills.get("jd", []),
    )
    reasoning = _reason_with_llm(state, matched_skills, missing_skills)

    return {
        "matched_skills": reasoning.matched_skills,
        "missing_skills": reasoning.missing_skills,
        "improvement_actions": reasoning.improvement_actions,
        "summary": reasoning.summary,
        "llm_score": reasoning.llm_score,
    }


llm_reasoning_agent = RunnableLambda(llm_reasoning_agent_fn)
