from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from utils.text import clean_text, extract_text_from_pdf, split_blocks


@tool
def parse_resume_tool(resume_file) -> str:
    """Extract clean text from an uploaded resume PDF."""
    return clean_text(extract_text_from_pdf(resume_file))


def parser_agent_fn(state):
    try:
        resume_text = clean_text(extract_text_from_pdf(state["resume_file"]))
    except Exception as exc:
        return {"error": f"Could not parse resume: {exc}"}

    return {
        "resume_text": resume_text,
        "jd_text": clean_text(state["jd_text"]),
        "resume_chunks": split_blocks(resume_text),
    }


parser_agent = RunnableLambda(parser_agent_fn)
