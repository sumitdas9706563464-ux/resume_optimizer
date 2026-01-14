
import streamlit as st
import sys
import os
import tempfile

# Add the 'src' directory to the Python path to import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_extraction import extract_text_from_pdf
from src.text_preprocessing import preprocess_text
from src.keyword_extraction import extract_keywords
from src.similarity_scoring import calculate_similarity
from src.gap_analysis import analyze_gaps
from src.explainability import generate_explanations
from src.resume_updater import add_keywords_to_resume
from src.pdf_generation import generate_pdf

# --- Streamlit App UI ---
st.title("Interactive AI Resume Optimizer")

# --- Session State Initialization ---
# This helps maintain state across user interactions
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'missing_keywords' not in st.session_state:
    st.session_state.missing_keywords = []
if 'original_resume_text' not in st.session_state:
    st.session_state.original_resume_text = ""
if 'pdf_generated' not in st.session_state:
    st.session_state.pdf_generated = False
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = ""


# --- Step 1: User Inputs ---
st.header("Step 1: Provide Your Resume and Job Description")
uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze Resume"):
    if uploaded_resume and job_description:
        with st.spinner("Analyzing your resume against the job description..."):
            # Save uploaded PDF to a temporary file
            temp_dir = tempfile.gettempdir()
            temp_pdf_path = os.path.join(temp_dir, uploaded_resume.name)
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_resume.getbuffer())

            # --- NLP Pipeline Execution ---
            resume_text = extract_text_from_pdf(temp_pdf_path)
            st.session_state.original_resume_text = resume_text

            preprocessed_resume = preprocess_text(resume_text)
            preprocessed_jd = preprocess_text(job_description)

            resume_keywords = extract_keywords(preprocessed_resume)
            jd_keywords = extract_keywords(preprocessed_jd)

            similarity_score = calculate_similarity(preprocessed_resume, preprocessed_jd)
            gaps = analyze_gaps(resume_keywords, jd_keywords)
            explanations = generate_explanations(gaps)

            st.session_state.missing_keywords = gaps['missing_keywords']
            st.session_state.analysis_complete = True

            # --- Display Results ---
            st.header("Analysis Results")
            st.metric(label="Resume Match Score", value=f"{similarity_score:.2f}%")

            st.subheader("Missing Keywords & Suggestions")
            if not gaps['missing_keywords']:
                st.success("Excellent! Your resume aligns well with the key requirements of this job description.")
            else:
                for i, keyword in enumerate(gaps['missing_keywords']):
                    st.warning(f"**Missing Keyword:** {keyword}")
                    st.info(f"**Suggestion:** {explanations['missing'][i]}")

            os.remove(temp_pdf_path) # Clean up temp file
    else:
        st.error("Please upload a resume and provide a job description.")

# --- Step 2: Resume Update and Download ---
if st.session_state.analysis_complete and st.session_state.missing_keywords:
    st.header("Step 2: Optimize Your Resume")

    keywords_to_add = st.multiselect(
        "Select keywords to add to your resume's skills section:",
        options=st.session_state.missing_keywords
    )

    if st.button("Update Resume & Generate PDF"):
        if keywords_to_add:
            with st.spinner("Generating your optimized resume..."):
                updated_text = add_keywords_to_resume(st.session_state.original_resume_text, keywords_to_add)

                output_pdf_path = os.path.join(tempfile.gettempdir(), "Optimized_Resume.pdf")
                generate_pdf(updated_text, output_pdf_path)

                st.session_state.pdf_generated = True
                st.session_state.pdf_path = output_pdf_path
        else:
            st.warning("Please select at least one keyword to add.")

if st.session_state.pdf_generated:
    st.success("Your optimized resume is ready for download!")
    with open(st.session_state.pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download Optimized Resume",
            data=pdf_file,
            file_name="Optimized_Resume.pdf",
            mime="application/pdf"
        )
