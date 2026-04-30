import streamlit as st

from graph.pipeline import run_pipeline
from ui.dashboard import render_dashboard, render_hero, render_insights


st.set_page_config(
    page_title="AI Hiring Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom styling for premium feel
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #6c757d;
    }
    .css-18ni7ap { padding-top: 2rem; }
    .css-1d391kg { padding: 2rem 1rem; }
    h1, h2, h3 { margin-top: 1.5rem; margin-bottom: 0.75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    # Header section
    st.markdown("## 🤖 AI Hiring Intelligence Platform")
    st.markdown("*Fast, accurate resume analysis with evidence-backed scoring*")
    st.markdown("")

    # Input section in clean container
    with st.container():
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.markdown("**Resume**")
            resume_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

        with col2:
            st.markdown("**Job Description**")
            jd_text = st.text_area("Paste JD", height=160, label_visibility="collapsed")

    st.markdown("")
    analyze_button = st.button("🚀 Analyze Candidate", use_container_width=True, type="primary")

    if not analyze_button:
        return

    if not resume_file:
        st.error("📄 Please upload a resume PDF")
        return

    if not jd_text:
        st.error("📝 Please paste a job description")
        return

    # Analysis phase
    with st.spinner("⚙️ Running AI analysis..."):
        state = run_pipeline(resume_file, jd_text)

    if state.get("error"):
        st.error(f"Error: {state['error']}")
        return

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Results section
    render_hero(state)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    render_dashboard(state)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    render_insights(state)

    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown(
        "<div style='text-align: center; color: #95a5a6; font-size: 0.9rem; padding: 1rem;'>"
        "✨ Powered by LangGraph & AI Intelligence"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
