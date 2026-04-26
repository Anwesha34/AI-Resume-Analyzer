import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from chatbot import get_ai_suggestions

# ---------------- DOWNLOAD NLTK ----------------
nltk.download("punkt")
nltk.download("stopwords")

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

This tool uses **TF-IDF + Cosine Similarity + AI Suggestions**
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
            text += page.extract_text()

        return text

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- REMOVE STOPWORDS ----------------
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    filtered_words = [word for word in words if word not in stop_words]

    return " ".join(filtered_words)

# ---------------- MATCH SCORE ----------------
def calculate_similarity(resume_text, job_description):

    resume_processed = remove_stopwords(clean_text(resume_text))
    job_processed = remove_stopwords(clean_text(job_description))

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        [resume_processed, job_processed]
    )

    score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0] * 100

    return round(score, 2)

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
                ai_report = get_ai_suggestions(resume_text)

            st.markdown(f"""
            <div style="
                background:#111;
                color:white;
                padding:20px;
                border-radius:12px;
                line-height:1.8;
                font-size:16px;
            ">
            {ai_report}
            </div>
            """, unsafe_allow_html=True)

            # ---------------- DOWNLOAD ----------------
            st.download_button(
                label="📥 Download Report",
                data=ai_report,
                file_name="resume_report.txt",
                mime="text/plain"
            )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()