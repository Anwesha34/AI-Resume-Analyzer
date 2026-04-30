import matplotlib.pyplot as plt
import streamlit as st


def _short_text(text, max_chars=260):
    text = " ".join(str(text or "").split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


def verdict_for_score(score):
    if score >= 75:
        return "🟢 Excellent"
    if score >= 55:
        return "🟡 Good"
    return "🔴 Low"


def render_hero(state):
    """Premium hero section with key metrics and summary."""
    score = state.get("overall_score", 0.0)
    summary_lines = [
        line.strip()
        for line in state.get("summary", "").splitlines()
        if line.strip()
    ][:2]
    summary_text = " ".join(summary_lines) if summary_lines else "Ready for review"

    col1, col2, col3 = st.columns([1.2, 1, 2], gap="medium")

    with col1:
        st.metric(label="Overall Score", value=f"{score:.1f}%")

    with col2:
        st.metric(label="Verdict", value=verdict_for_score(score))

    with col3:
        st.markdown(f"**✓ Summary**  \n{_short_text(summary_text, 120)}")


def render_dashboard(state):
    """Graph dashboard with 2x2 grid layout."""
    graph_data = state.get("graph_data", {})
    skill_match = graph_data.get("skill_match", {})
    category_scores = graph_data.get("category_scores") or state.get("section_scores", {})
    gap_analysis = graph_data.get("gap_analysis", {})

    st.markdown("### 📊 Analysis Dashboard")
    st.markdown("")

    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")

    # Row 1: Score bar chart
    with row1_col1:
        fig, ax = plt.subplots(figsize=(7, 2.2), facecolor="white")
        score_val = state.get("overall_score", 0)
        colors = ["#2ecc71" if score_val >= 75 else "#f39c12" if score_val >= 55 else "#e74c3c"]
        ax.barh(["Match Score"], [score_val], color=colors, height=0.5)
        ax.set_xlim(0, 100)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("Score (%)", fontsize=10)
        ax.set_title("Overall Match Score", fontsize=12, fontweight="bold", pad=10)
        ax.tick_params(left=False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Row 1: Skill match chart
    with row1_col2:
        fig, ax = plt.subplots(figsize=(7, 2.2), facecolor="white")
        matched = skill_match.get("matched", len(state.get("matched_skills", [])))
        missing = skill_match.get("missing", len(state.get("missing_skills", [])))
        bars = ax.bar(["✓ Matched", "✗ Missing"], [matched, missing], color=["#2ecc71", "#e74c3c"], width=0.6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title("Skill Breakdown", fontsize=12, fontweight="bold", pad=10)
        ax.set_ylim(0, max(matched, missing) * 1.2 if max(matched, missing) > 0 else 10)
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{int(height)}", ha="center", va="bottom", fontsize=9)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Row 2: Category scores
    with row2_col1:
        fig, ax = plt.subplots(figsize=(7, 2.8), facecolor="white")
        if category_scores:
            labels = list(category_scores.keys())[:8]
            values = list(category_scores.values())[:8]
            ax.bar(labels, values, color="#3498db", width=0.7)
            ax.set_ylim(0, 100)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.set_ylabel("Score", fontsize=10)
            ax.set_title("Category Scores", fontsize=12, fontweight="bold", pad=10)
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Row 2: Gap distribution
    with row2_col2:
        fig, ax = plt.subplots(figsize=(7, 2.8), facecolor="white")
        if gap_analysis:
            gap_labels = list(gap_analysis.keys())[:8]
            gap_values = list(gap_analysis.values())[:8]
            ax.barh(gap_labels, gap_values, color="#e67e22", height=0.6)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.set_xlabel("Count", fontsize=10)
            ax.set_title("Skill Gaps", fontsize=12, fontweight="bold", pad=10)
        else:
            ax.text(0.5, 0.5, "No gaps identified", ha="center", va="center", fontsize=11, color="#7f8c8d")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis("off")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def render_insights(state):
    """Skill intelligence, actions, evidence, and summary sections."""

    # Skill Intelligence Section
    st.markdown("")
    st.markdown("### 🎯 Skill Intelligence")
    st.markdown("")

    skill_col1, skill_col2 = st.columns(2, gap="medium")

    with skill_col1:
        st.markdown("#### ✅ Matched Skills")
        matched_skills = state.get("matched_skills", [])[:12]
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"• {skill}")
        else:
            st.info("No direct skill matches found")

    with skill_col2:
        st.markdown("#### ❌ Missing Skills")
        missing_skills = state.get("missing_skills", [])[:12]
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"• {skill}")
        else:
            st.info("No major missing skills identified")

    # Improvement Actions Section
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown("### 💡 Recommended Actions")

    actions = state.get("improvement_actions", [])[:8]
    if actions:
        for idx, action in enumerate(actions, 1):
            st.markdown(f"{idx}. {action}")
    else:
        st.info("No improvement actions available")

    # Evidence Mapping Section
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown("### 📋 Evidence Mapping")
    st.markdown("*Top matches between job description and resume*")
    st.markdown("")

    evidence_items = state.get("evidence_mapping", [])[:5]
    if evidence_items:
        for idx, item in enumerate(evidence_items, 1):
            with st.container(border=True):
                col_status, col_content = st.columns([0.12, 0.88], gap="small")

                status = item.get("status", "missing").lower()
                if status == "matched":
                    col_status.markdown("✅")
                else:
                    col_status.markdown("⚠️")

                with col_content:
                    st.markdown(f"**{_short_text(item.get('jd_requirement', ''), 180)}**")
                    st.caption(f"📝 {_short_text(item.get('resume_evidence') or 'No evidence found', 240)}")

    else:
        st.info("No evidence mapping available")

    # Quick Summary Section
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown("### 📄 Quick Summary")
    summary_lines = [
        line.strip()
        for line in state.get("summary", "").splitlines()
        if line.strip()
    ][:3]

    if summary_lines:
        for line in summary_lines:
            st.markdown(f"• {_short_text(line, 200)}")
    else:
        st.info("No summary available")
