
import streamlit as st
import sys
import os
import tempfile

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_extraction import extract_text
from src.text_preprocessing import preprocess_text
from src.keyword_extraction import extract_keywords, categorize_keywords
from src.similarity_scoring import calculate_similarity
from src.ats_scoring import calculate_ats_score
from src.gap_analysis import analyze_gaps
from src.resume_updater import add_keywords_to_resume
from src.document_generation import generate_pdf, generate_docx

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Optimizer Pro",
    page_icon="🚀",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        border-radius: 5px;
        height: 3em;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .keyword-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        background-color: #e1f5fe;
        color: #0288d1;
        font-size: 0.8em;
        margin: 2px;
        border: 1px solid #b3e5fc;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'optimized' not in st.session_state:
    st.session_state.optimized = False
if 'original_score' not in st.session_state:
    st.session_state.original_score = 0
if 'optimized_score' not in st.session_state:
    st.session_state.optimized_score = 0
if 'missing_keywords' not in st.session_state:
    st.session_state.missing_keywords = []
if 'categorized_missing' not in st.session_state:
    st.session_state.categorized_missing = {}
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'optimized_text' not in st.session_state:
    st.session_state.optimized_text = ""
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""

# --- Sidebar ---
with st.sidebar:
    st.title("🚀 Resume Pro")
    st.markdown("Optimize your resume for ATS systems in seconds.")
    st.divider()

    uploaded_resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    uploaded_jd = st.file_uploader("Upload Job Description", type=["pdf", "docx"])
    job_description_text = st.text_area("Or Paste Job Description", height=150)

    analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True, type="primary")

# --- Main Content ---
st.title("AI-Powered ATS Optimizer")

if analyze_btn:
    if uploaded_resume and (uploaded_jd or job_description_text):
        with st.spinner("Analyzing match..."):
            temp_dir = tempfile.gettempdir()

            # Extract Resume Text
            temp_resume_path = os.path.join(temp_dir, uploaded_resume.name)
            with open(temp_resume_path, "wb") as f:
                f.write(uploaded_resume.getbuffer())
            st.session_state.resume_text = extract_text(temp_resume_path)

            # Extract JD Text
            if uploaded_jd:
                temp_jd_path = os.path.join(temp_dir, uploaded_jd.name)
                with open(temp_jd_path, "wb") as f:
                    f.write(uploaded_jd.getbuffer())
                st.session_state.jd_text = extract_text(temp_jd_path)
            else:
                st.session_state.jd_text = job_description_text

            # NLP Pipeline
            preprocessed_resume = preprocess_text(st.session_state.resume_text)
            preprocessed_jd = preprocess_text(st.session_state.jd_text)

            jd_keywords = extract_keywords(preprocessed_jd)
            resume_keywords = extract_keywords(preprocessed_resume)

            gaps = analyze_gaps(resume_keywords, jd_keywords)
            st.session_state.missing_keywords = gaps['missing_keywords']
            st.session_state.categorized_missing = categorize_keywords(gaps['missing_keywords'])

            # Scoring
            st.session_state.original_score, st.session_state.feedback = calculate_ats_score(
                st.session_state.resume_text,
                jd_keywords
            )

            st.session_state.analysis_complete = True
            st.session_state.optimized = False # Reset optimization if new analysis
    else:
        st.error("Please provide both a resume and a job description.")

if st.session_state.analysis_complete:
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🛠️ Optimization", "📥 Download"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Score", f"{st.session_state.original_score}%")
        with col2:
            match_score = calculate_similarity(preprocess_text(st.session_state.resume_text), preprocess_text(st.session_state.jd_text))
            st.metric("JD Match", f"{match_score:.1f}%")
        with col3:
            st.metric("Missing Keywords", len(st.session_state.missing_keywords))

        st.subheader("ATS Feedback")
        for item in st.session_state.feedback:
            if "excellent" in item.lower() or "good" in item.lower():
                st.success(item)
            else:
                st.warning(item)

        st.subheader("Missing Keywords by Category")
        cat_cols = st.columns(len(st.session_state.categorized_missing))
        for i, (cat, words) in enumerate(st.session_state.categorized_missing.items()):
            with cat_cols[i]:
                st.write(f"**{cat}**")
                if words:
                    for word in words:
                        st.markdown(f"<span class='keyword-tag'>{word}</span>", unsafe_allow_html=True)
                else:
                    st.write("None missing!")

    with tab2:
        st.subheader("Enhance Your Resume")
        st.write("Select the keywords you want to naturally integrate into your resume.")

        selected_keywords = st.multiselect(
            "Keywords to add (~30 recommended for best results)",
            options=st.session_state.missing_keywords,
            default=st.session_state.missing_keywords[:min(30, len(st.session_state.missing_keywords))]
        )

        if st.button("🚀 Optimize Resume Now", use_container_width=True, type="primary"):
            with st.spinner("Generating optimized version..."):
                st.session_state.optimized_text = add_keywords_to_resume(st.session_state.resume_text, selected_keywords)

                # Re-calculate score
                preprocessed_jd = preprocess_text(st.session_state.jd_text)
                jd_keywords = extract_keywords(preprocessed_jd)
                st.session_state.optimized_score, _ = calculate_ats_score(st.session_state.optimized_text, jd_keywords)
                st.session_state.optimized = True

        if st.session_state.optimized:
            st.success("Resume Optimized!")
            c1, c2 = st.columns(2)
            c1.metric("Original Score", f"{st.session_state.original_score}%")
            c2.metric("Optimized Score", f"{st.session_state.optimized_score}%", delta=f"{st.session_state.optimized_score - st.session_state.original_score}%")

            with st.expander("Preview Optimized Text"):
                st.text(st.session_state.optimized_text)

    with tab3:
        if st.session_state.optimized:
            st.subheader("Download Production-Ready Resume")
            st.write("These files are formatted to be 100% ATS-friendly.")

            col_pdf, col_docx = st.columns(2)

            # PDF Generation
            pdf_path = os.path.join(tempfile.gettempdir(), "Optimized_Resume_Pro.pdf")
            generate_pdf(st.session_state.optimized_text, pdf_path)
            with open(pdf_path, "rb") as f:
                col_pdf.download_button(
                    "Download PDF",
                    data=f,
                    file_name="Optimized_Resume_Pro.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            # DOCX Generation
            docx_path = os.path.join(tempfile.gettempdir(), "Optimized_Resume_Pro.docx")
            generate_docx(st.session_state.optimized_text, docx_path)
            with open(docx_path, "rb") as f:
                col_docx.download_button(
                    "Download DOCX",
                    data=f,
                    file_name="Optimized_Resume_Pro.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.info("Please optimize your resume in the 'Optimization' tab first.")
else:
    st.info("Upload your resume and a job description to begin the analysis.")
