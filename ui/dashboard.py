import matplotlib.pyplot as plt
import streamlit as st


def _short_text(text, max_chars=260):
    text = " ".join(str(text or "").split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


def verdict_for_score(score):
    if score >= 75:
        return "Excellent"
    if score >= 55:
        return "Good"
    return "Low"


def _render_bullets(items, empty_message):
    for item in items or [empty_message]:
        st.write(f"- {item}")


def render_hero(state):
    score = state.get("overall_score", 0.0)
    summary_lines = [
        line.strip()
        for line in state.get("summary", "").splitlines()
        if line.strip()
    ][:2]

    score_col, verdict_col, summary_col = st.columns([1, 1, 3])

    with score_col:
        st.metric("Overall Score", f"{score:.2f}%")

    with verdict_col:
        st.metric("Verdict", verdict_for_score(score))

    with summary_col:
        st.markdown("**Recruiter Summary**")
        _render_bullets(summary_lines, "No summary returned.")


def render_dashboard(state):
    graph_data = state.get("graph_data", {})
    score_distribution = graph_data.get("score_distribution", {})
    skill_match = graph_data.get("skill_match", {})
    category_scores = graph_data.get("category_scores") or state.get("section_scores", {})
    gap_analysis = graph_data.get("gap_analysis", {})

    st.subheader("Dashboard")

    top_left, top_right = st.columns(2)
    bottom_left, bottom_right = st.columns(2)

    fig, ax = plt.subplots(figsize=(7, 1.4))
    ax.barh(["Overall"], [state.get("overall_score", 0)])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title("Score Bar")
    top_left.pyplot(fig)
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
    top_right.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(category_scores.keys(), category_scores.values())
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")
    ax.set_title("Category Breakdown")
    ax.tick_params(axis="x", rotation=20)
    bottom_left.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 3))
    gap_labels = list(gap_analysis) or ["No major gaps"]
    gap_values = list(gap_analysis.values()) or [0]
    ax.barh(gap_labels, gap_values)
    ax.set_xlabel("Count")
    ax.set_title("Gap Analysis")
    bottom_right.pyplot(fig)
    plt.close(fig)

    if score_distribution:
        with st.expander("Score Signals"):
            _render_bullets(
                [f"{name}: {value}" for name, value in score_distribution.items()],
                "No score signals returned.",
            )


def render_insights(state):
    st.subheader("Skill Intelligence")
    matched_col, missing_col = st.columns(2)

    with matched_col:
        st.markdown("**Matched Skills**")
        _render_bullets(
            [f"\u2705 {skill}" for skill in state.get("matched_skills", [])[:12]],
            "No direct skill matches found.",
        )

    with missing_col:
        st.markdown("**Missing Skills**")
        _render_bullets(
            [f"\u274c {skill}" for skill in state.get("missing_skills", [])[:12]],
            "No major missing skills found.",
        )

    st.markdown("---")
    st.subheader("Improvement Actions")
    _render_bullets(state.get("improvement_actions", [])[:8], "No improvement actions returned.")

    st.markdown("---")
    st.subheader("Evidence Mapping")
    for item in state.get("evidence_mapping", [])[:5]:
        with st.container(border=True):
            st.markdown("**JD Requirement:**")
            st.write(_short_text(item.get("jd_requirement", ""), 220))

            st.markdown("**Resume Evidence:**")
            st.write(_short_text(item.get("resume_evidence") or "No matching resume evidence found.", 260))

            st.markdown("**Status:**")
            st.write(item.get("status", "").title() or "Missing")
