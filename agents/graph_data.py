from langchain_core.runnables import RunnableLambda

from llm.client import invoke_structured
from llm.schemas import GraphDataOutput


def _fallback_graph_data(state):
    matched_skills = state.get("matched_skills", [])
    missing_skills = state.get("missing_skills", [])
    return GraphDataOutput(
        score_distribution={
            "Semantic": state.get("semantic_score", 0.0),
            "Skill Match": state.get("skill_match_score", 0.0),
            "LLM": state.get("llm_score", 0.0),
            "Overall": state.get("overall_score", 0.0),
        },
        skill_match={
            "matched": len(matched_skills),
            "missing": len(missing_skills),
        },
        category_scores=state.get("section_scores", {}),
        gap_analysis={
            skill: 1 for skill in missing_skills[:8]
        },
    )


def graph_data_agent_fn(state):
    template = """
Create compact graph data. Numeric JSON only. Mirror section scores in category_scores.

Overall score:
{overall_score}

Semantic score:
{semantic_score}

Skill match score:
{skill_match_score}

LLM score:
{llm_score}

Section scores:
{section_scores}

Matched skills: {matched_skills}
Missing skills: {missing_skills}

{format_instructions}
"""
    graph_data = invoke_structured(
        GraphDataOutput,
        template,
        fallback=_fallback_graph_data(state),
        overall_score=state.get("overall_score", 0.0),
        semantic_score=state.get("semantic_score", 0.0),
        skill_match_score=state.get("skill_match_score", 0.0),
        llm_score=state.get("llm_score", 0.0),
        section_scores=state.get("section_scores", {}),
        matched_skills=state.get("matched_skills", [])[:10],
        missing_skills=state.get("missing_skills", [])[:10],
    )

    if hasattr(graph_data, "model_dump"):
        return {"graph_data": graph_data.model_dump()}

    return {"graph_data": graph_data.dict()}


graph_data_agent = RunnableLambda(graph_data_agent_fn)
