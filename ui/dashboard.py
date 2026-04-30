import matplotlib.pyplot as plt
import streamlit as st


def verdict_for_score(score):
    if score >= 75:
        return "Excellent"
    if score >= 55:
        return "Good"
    return "Low"


def _render_bullets(items, empty_message):
    for item in items or [empty_message]:
        st.write(f"- {item}")


def render_dashboard(state):
    graph_data = state.get("graph_data", {})
    score_distribution = graph_data.get("score_distribution", {})
    skill_match = graph_data.get("skill_match", {})
    category_scores = graph_data.get("category_scores") or state.get("section_scores", {})
    gap_analysis = graph_data.get("gap_analysis", {})

    st.subheader("Dashboard")

    fig, ax = plt.subplots(figsize=(7, 1.4))
    ax.barh(["Overall"], [state.get("overall_score", 0)])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title("Score Bar")
    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(
        ["Matched", "Missing"],
        [
            skill_match.get("matched", len(state.get("matched_skills", []))),
            skill_match.get("missing", len(state.get("missing_skills", []))),
        ],
    )
    ax.set_ylabel("Skills")
    ax.set_title("Skill Match")
    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(category_scores.keys(), category_scores.values())
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")
    ax.set_title("Category Breakdown")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 3))
    gap_labels = list(gap_analysis) or ["No major gaps"]
    gap_values = list(gap_analysis.values()) or [0]
    ax.barh(gap_labels, gap_values)
    ax.set_xlabel("Count")
    ax.set_title("Gap Analysis")
    st.pyplot(fig)
    plt.close(fig)

    if score_distribution:
        with st.expander("Score Signals"):
            _render_bullets(
                [f"{name}: {value}" for name, value in score_distribution.items()],
                "No score signals returned.",
            )


def render_insights(state):
    st.subheader("Matched Skills")
    _render_bullets(state.get("matched_skills", [])[:12], "No direct skill matches found.")

    st.subheader("Missing Skills")
    _render_bullets(state.get("missing_skills", [])[:12], "No major missing skills found.")

    st.subheader("Improvement Actions")
    _render_bullets(state.get("improvement_actions", [])[:8], "No improvement actions returned.")

    st.subheader("Evidence Mapping")
    for item in state.get("evidence_mapping", []):
        st.write(f"JD: {item.get('jd_requirement', '')}")
        st.write(f"Resume: {item.get('resume_evidence') or 'No matching resume evidence found.'}")
        st.write(f"Status: {item.get('status', '').title()}")
        st.divider()

    st.subheader("Summary")
    summary_lines = [line.strip() for line in state.get("summary", "").splitlines() if line.strip()]
    _render_bullets(summary_lines[:2], "No summary returned.")
