from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from llm.client import invoke_structured
from llm.schemas import SkillValidation
from utils.models import get_ner_model


def _extract_entities(text):
    model = get_ner_model()
    entities = model((text or "")[:12000])
    skills = []

    for entity in entities:
        value = entity.get("word", "").replace("##", "").strip()
        if value and value not in skills:
            skills.append(value)

    return skills


@tool
def transformer_skill_tool(text: str) -> list:
    """Extract raw skill and concept candidates with a transformer NER model."""
    return _extract_entities(text)


def validate_skills_with_llm(resume_text, jd_text, raw_resume_skills, raw_jd_skills):
    template = """
Normalize technical skills. Use only provided context. Expand grounded abbreviations. No invented skills.

Resume context:
{resume_context}

JD requirements:
{jd_requirements}

Resume entities:
{raw_resume_skills}

JD entities:
{raw_jd_skills}

{format_instructions}
"""
    return invoke_structured(
        SkillValidation,
        template,
        fallback=SkillValidation(
            resume_skills=raw_resume_skills,
            jd_skills=raw_jd_skills,
        ),
        resume_context=resume_text,
        jd_requirements=jd_text,
        raw_resume_skills=raw_resume_skills,
        raw_jd_skills=raw_jd_skills,
    )


def extract_structured_resume_data(text, raw_skills):
    return {
        "skills": raw_skills[:30],
        "highlights": [
            line.strip()
            for line in (text or "").splitlines()
            if line.strip()
        ][:8],
    }


def skill_extraction_agent_fn(state):
    raw_resume_skills = transformer_skill_tool.invoke(state["resume_text"])
    raw_jd_skills = transformer_skill_tool.invoke(state["jd_text"])
    resume_context = "\n".join(state.get("relevant_resume_chunks") or state.get("resume_chunks", [])[:5])
    jd_context = "\n".join(state.get("jd_requirements", [])) or state["jd_text"]
    validated = validate_skills_with_llm(
        resume_context,
        jd_context,
        raw_resume_skills,
        raw_jd_skills,
    )

    return {
        "extracted_skills": {
            "raw_resume": raw_resume_skills,
            "raw_jd": raw_jd_skills,
            "resume": validated.resume_skills,
            "jd": validated.jd_skills,
        },
        "structured_resume_data": extract_structured_resume_data(
            resume_context,
            validated.resume_skills,
        ),
    }


skill_extraction_agent = RunnableLambda(skill_extraction_agent_fn)
