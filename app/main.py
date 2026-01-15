
"""
This is the main script for the Interactive AI Resume Optimizer application.
It uses Streamlit to create a web-based user interface for resume analysis and optimization.
"""

import streamlit as st
import sys
import os
import tempfile

# Add the 'src' directory to the Python path to import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_extraction import extract_text
from src.text_preprocessing import preprocess_text
from src.keyword_extraction import extract_keywords
from src.similarity_scoring import calculate_similarity
from src.ats_scoring import calculate_ats_score
from src.gap_analysis import analyze_gaps
from src.explainability import generate_explanations
from src.resume_updater import add_keywords_to_resume
from src.document_generation import generate_pdf, generate_docx

# --- Page Configuration ---
st.set_page_config(
    page_title="ATS Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

# --- Session State Initialization ---
# This helps maintain state across user interactions
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'missing_keywords' not in st.session_state:
    st.session_state.missing_keywords = []
if 'original_resume_text' not in st.session_state:
    st.session_state.original_resume_text = ""
if 'file_generated' not in st.session_state:
    st.session_state.file_generated = False
if 'generated_pdf_path' not in st.session_state:
    st.session_state.generated_pdf_path = ""
if 'generated_docx_path' not in st.session_state:
    st.session_state.generated_docx_path = ""

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.title("📄 ATS Resume Optimizer")
    st.markdown("---")
    st.header("Upload Your Files")
    uploaded_resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
    uploaded_jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"])
    job_description_text = st.text_area("Or Paste the Job Description here", height=200)

    st.markdown("---")
    analyze_button = st.button("Analyze Resume", use_container_width=True)

# --- Main Panel for Displaying Results ---
st.title("AI-Powered Resume Analysis")

# This block executes when the user clicks the "Analyze Resume" button
if analyze_button:
    if uploaded_resume and (uploaded_jd or job_description_text):
        with st.spinner("Analyzing your resume..."):
            temp_dir = tempfile.gettempdir()

            # Process uploaded resume
            temp_resume_path = os.path.join(temp_dir, uploaded_resume.name)
            with open(temp_resume_path, "wb") as f:
                f.write(uploaded_resume.getbuffer())
            resume_text = extract_text(temp_resume_path)
            st.session_state.original_resume_text = resume_text

            # Process job description from file or text area
            jd_text = ""
            temp_jd_path = None
            if uploaded_jd:
                temp_jd_path = os.path.join(temp_dir, uploaded_jd.name)
                with open(temp_jd_path, "wb") as f:
                    f.write(uploaded_jd.getbuffer())
                jd_text = extract_text(temp_jd_path)
            else:
                jd_text = job_description_text

            # --- NLP Pipeline Execution ---
            # The following steps perform the core analysis of the resume and job description
            ats_score, ats_feedback = calculate_ats_score(resume_text)
            preprocessed_resume = preprocess_text(resume_text)
            preprocessed_jd = preprocess_text(jd_text)
            resume_keywords = extract_keywords(preprocessed_resume)
            jd_keywords = extract_keywords(preprocessed_jd)
            similarity_score = calculate_similarity(preprocessed_resume, preprocessed_jd)
            gaps = analyze_gaps(resume_keywords, jd_keywords)
            explanations = generate_explanations(gaps)
            st.session_state.missing_keywords = gaps['missing_keywords']
            st.session_state.analysis_complete = True

            # --- Display Results ---
            # The results are displayed in two columns for a clean layout
            col1, col2 = st.columns(2)
            with col1:
                st.header("ATS Score")
                st.metric(label="Your Resume's ATS Score", value=f"{ats_score}%")
                with st.expander("See detailed feedback"):
                    for feedback_item in ats_feedback:
                        st.warning(feedback_item)

            with col2:
                st.header("Job Description Match")
                st.metric(label="Resume Match Score", value=f"{similarity_score:.2f}%")

            st.markdown("---")
            st.header("Missing Keywords & Suggestions")
            if not gaps['missing_keywords']:
                st.success("Excellent! Your resume aligns well with the key requirements.")
            else:
                for i, keyword in enumerate(gaps['missing_keywords']):
                    st.warning(f"**Missing Keyword:** {keyword}")
                    st.info(f"**Suggestion:** {explanations['missing'][i]}")

            # Clean up temporary files to save space
            os.remove(temp_resume_path)
            if temp_jd_path:
                os.remove(temp_jd_path)
    else:
        st.error("Please upload a resume and provide a job description.")

# This block executes after the analysis is complete
if st.session_state.analysis_complete:
    st.markdown("---")
    st.header("Optimize Your Resume")

    keywords_to_add = st.multiselect(
        "Select keywords to add to your resume's skills section:",
        options=st.session_state.missing_keywords
    )

    if st.button("Update Resume & Generate Files", use_container_width=True):
        if keywords_to_add:
            with st.spinner("Generating your optimized resume..."):
                updated_text = add_keywords_to_resume(st.session_state.original_resume_text, keywords_to_add)

                # Generate both PDF and DOCX files for download
                output_pdf_path = os.path.join(tempfile.gettempdir(), "Optimized_Resume.pdf")
                generate_pdf(updated_text, output_pdf_path)
                st.session_state.generated_pdf_path = output_pdf_path

                output_docx_path = os.path.join(tempfile.gettempdir(), "Optimized_Resume.docx")
                generate_docx(updated_text, output_docx_path)
                st.session_state.generated_docx_path = output_docx_path

                st.session_state.file_generated = True
        else:
            st.warning("Please select at least one keyword to add.")

# This block executes after the optimized resume has been generated
if st.session_state.file_generated:
    st.markdown("---")
    st.header("Download Your Optimized Resume")

    download_format = st.radio(
        "Choose your preferred download format:",
        ('PDF', 'DOCX'),
        horizontal=True
    )

    # Provide download buttons for both PDF and DOCX formats
    if download_format == 'PDF':
        with open(st.session_state.generated_pdf_path, "rb") as file:
            st.download_button(
                label="Download Optimized Resume (PDF)",
                data=file,
                file_name="Optimized_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    elif download_format == 'DOCX':
        with open(st.session_state.generated_docx_path, "rb") as file:
            st.download_button(
                label="Download Optimized Resume (DOCX)",
                data=file,
                file_name="Optimized_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
