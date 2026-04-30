from langchain_core.runnables import RunnableLambda

from llm.client import invoke_structured
from llm.schemas import ScoringOutput


def _skill_match_score(state):
    matched = len(state.get("matched_skills", []))
    missing = len(state.get("missing_skills", []))
    total = matched + missing
    return (matched / total) * 100 if total else 0.0


def _dynamic_section_scores(state):
    template = """
Generate dynamic category scores. Choose job-relevant category names. Scores 0-100. Use only provided evidence.

JD requirements:
{jd_requirements}

Matched skills:
{matched_skills}

Missing skills:
{missing_skills}

Evidence mapping:
{evidence_mapping}

{format_instructions}
"""
    return invoke_structured(
        ScoringOutput,
        template,
        fallback=ScoringOutput(section_scores=_fallback_section_scores(state)),
        jd_requirements=state.get("jd_requirements", [])[:7],
        matched_skills=state.get("matched_skills", []),
        missing_skills=state.get("missing_skills", []),
        evidence_mapping=state.get("evidence_mapping", [])[:5],
    )


def _fallback_section_scores(state):
    evidence_mapping = state.get("evidence_mapping", [])
    if not evidence_mapping:
        return {"Role Alignment": 0.0}

    matched = sum(1 for item in evidence_mapping if item.get("status") == "matched")
    return {
        "Evidence Coverage": round((matched / len(evidence_mapping)) * 100, 2),
        "Skill Coverage": round(_skill_match_score(state), 2),
    }


def scoring_agent_fn(state):
    semantic_score = state.get("semantic_score", 0.0)
    skill_score = _skill_match_score(state)
    llm_score = state.get("llm_score", 0.0)
    overall_score = (semantic_score * 0.6) + (skill_score * 0.2) + (llm_score * 0.2)
    scoring = _dynamic_section_scores(state)

    return {
        "skill_match_score": round(skill_score, 2),
        "section_scores": scoring.section_scores,
        "overall_score": round(max(0.0, min(overall_score, 100.0)), 2),
    }


scoring_agent = RunnableLambda(scoring_agent_fn)
