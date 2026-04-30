import re
from io import BytesIO

import matplotlib.pyplot as plt
import PyPDF2
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sentence_transformers import SentenceTransformer, util

from chatbot import format_ai_suggestions, get_ai_suggestions


# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📄 AI Resume Job Match Analyzer")
st.markdown("""
Upload your resume (PDF) and paste a job description to check how well your resume matches.

This tool uses **Semantic Embeddings + AI Suggestions**
""")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("About")
    st.info("""
This tool helps you:

✅ Match your resume with job description  
✅ Get resume score  
✅ AI suggestions to improve resume  
✅ Download final report
""")

    st.header("How It Works")
    st.write("""
1. Upload Resume PDF  
2. Paste Job Description  
3. Click Analyze  
4. View Score + Suggestions
""")


# ---------------- PDF TEXT EXTRACT ----------------
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def split_resume_chunks(resume_text):
    raw_chunks = re.split(r"\n\s*\n|\n", resume_text)
    chunks = []
    current_chunk = []
    current_length = 0

    for raw_chunk in raw_chunks:
        chunk = clean_text(raw_chunk)
        if not chunk:
            continue

        current_chunk.append(chunk)
        current_length += len(chunk)

        if current_length >= 180:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks or [clean_text(resume_text)]


# ---------------- MATCH SCORE ----------------
def calculate_similarity(resume_text, job_description):
    resume_chunks = split_resume_chunks(resume_text)
    job_text = clean_text(job_description)

    if not job_text or not resume_chunks:
        return 0.0

    model = load_embedding_model()
    resume_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    chunk_scores = util.cos_sim(resume_embeddings, job_embedding).flatten()
    average_score = chunk_scores.mean().item() * 100

    return round(max(0, min(average_score, 100)), 2)


def create_pdf(report_text):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    # Write each line
    for line in report_text.split("\n"):
        pdf.drawString(50, y, line)
        y -= 20

        # New page if space ends
        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)

    return buffer


# ---------------- MAIN APP ----------------
def main():

    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=220
    )

    if st.button("Analyze Match"):

        if not uploaded_file:
            st.warning("Please upload your resume.")
            return

        if not job_description:
            st.warning("Please paste job description.")
            return

        with st.spinner("Analyzing Resume..."):

            # Extract Resume Text
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                st.error("Could not read resume.")
                return

            # Calculate Match Score
            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )

            # ---------------- RESULT ----------------
            st.subheader("📊 Match Results")

            st.metric(
                label="Resume Match Score",
                value=f"{similarity_score:.2f}%"
            )

            # ---------------- BAR GRAPH ----------------
            fig, ax = plt.subplots(figsize=(8, 0.8))

            colors = ['#ff4b4b', '#ffa726', '#0f9d58']
            color_index = min(int(similarity_score // 33), 2)

            ax.barh(
                [0],
                [similarity_score],
                color=colors[color_index]
            )

            ax.set_xlim(0, 100)
            ax.set_yticks([])
            ax.set_xlabel("Match Percentage")
            ax.set_title("Resume Job Match Score")

            st.pyplot(fig)

            # ---------------- SCORE MESSAGE ----------------
            if similarity_score < 40:
                st.warning(
                    "Low Match. Tailor your resume more closely."
                )

            elif similarity_score < 70:
                st.info(
                    "Good Match. Resume aligns fairly well."
                )

            else:
                st.success(
                    "Excellent Match! Strong alignment."
                )

            # ---------------- AI REPORT ----------------
            st.subheader("🤖 AI Generated Analysis Report")

            with st.spinner("Generating Suggestions..."):
                ai_suggestions = get_ai_suggestions(resume_text, job_description)
                ai_report = format_ai_suggestions(ai_suggestions)

            st.markdown(f"""
            <div style="
                background:#111;
                color:white;
                padding:20px;
                border-radius:12px;
                line-height:1.8;
                font-size:16px;
                white-space:pre-wrap;
            ">
            {ai_report}
            </div>
            """, unsafe_allow_html=True)

            # ---------------- DOWNLOAD ----------------
            pdf_file = create_pdf(ai_report)

            st.download_button(
                label="📥 Download Report (PDF)",
                data=pdf_file,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()
