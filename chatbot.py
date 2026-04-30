import os
from typing import List

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

api = os.environ["GROQ_API_KEY"]

llm = ChatGroq(
    api_key=api,
    model_name="llama-3.1-8b-instant"
)


class ResumeSuggestions(BaseModel):
    missing_skills: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    summary: str = ""


def get_ai_suggestions(resume_text, job_description=""):
    parser = PydanticOutputParser(pydantic_object=ResumeSuggestions)

    prompt = PromptTemplate(
        input_variables=["resume", "job_description"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""
You are an experienced technical recruiter and resume reviewer.

Compare the resume against the job description. Give practical, specific feedback.
Focus on missing skills, measurable improvements, ATS wording, and role alignment.
Do not invent experience that is not present in the resume.

Resume:
{resume}

Job description:
{job_description}

{format_instructions}
"""
    )

    response = llm.invoke(
        prompt.format(
            resume=resume_text,
            job_description=job_description or "No job description provided."
        )
    )

    try:
        return parser.parse(response.content)
    except Exception:
        return ResumeSuggestions(
            improvements=[
                "Review the resume for clearer role alignment, stronger action verbs, and measurable project outcomes."
            ],
            summary=response.content.strip()
        )


def format_ai_suggestions(suggestions):
    missing_skills = "\n".join(f"- {skill}" for skill in suggestions.missing_skills)
    improvements = "\n".join(f"- {item}" for item in suggestions.improvements)

    return f"""Summary
{suggestions.summary}

Missing Skills
{missing_skills or "- No major missing skills identified."}

Improvements
{improvements or "- No major improvements identified."}
"""
