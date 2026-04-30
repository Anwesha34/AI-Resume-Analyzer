import streamlit as st

from graph.pipeline import run_pipeline
from ui.dashboard import render_dashboard, render_insights, verdict_for_score


st.set_page_config(
    page_title="AI Hiring Intelligence Platform",
    page_icon="AI",
    layout="wide",
)


def main():
    st.title("AI Hiring Intelligence Platform")
    st.caption("LangGraph-orchestrated resume evaluation with grounded evidence and recruiter-ready insights.")

    with st.sidebar:
        st.header("Workflow")
        st.write("1. Upload resume")
        st.write("2. Paste job description")
        st.write("3. Review score, evidence, and gaps")

    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    jd_text = st.text_area("Paste Job Description", height=240)

    if not st.button("Analyze Candidate"):
        return

    if not resume_file:
        st.warning("Please upload a resume PDF.")
        return

    if not jd_text:
        st.warning("Please paste a job description.")
        return

    with st.spinner("Running hiring intelligence graph..."):
        state = run_pipeline(resume_file, jd_text)

    if state.get("error"):
        st.error(state["error"])
        return

    score = state.get("overall_score", 0.0)
    summary = state.get("summary", "")

    st.subheader("Hiring Fit")
    st.metric("Overall Score", f"{score:.2f}%")
    st.write(f"Verdict: {verdict_for_score(score)}")

    summary_lines = [line.strip() for line in summary.splitlines() if line.strip()]
    for line in summary_lines[:2]:
        st.write(f"- {line}")

    render_dashboard(state)
    render_insights(state)


if __name__ == "__main__":
    main()
