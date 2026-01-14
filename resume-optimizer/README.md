
# Interactive AI Resume Optimizer

This project is a Streamlit web application that helps users optimize their resumes for a specific job description. It uses NLP techniques to compare a resume to a job description, identify missing keywords, and suggest improvements.

## Features

-   **Resume vs. Job Description Analysis:** Compares your resume (PDF) against a job description.
-   **Similarity Score:** Calculates a relevance score to show how well your resume matches the job.
-   **Keyword Gap Analysis:** Identifies important keywords from the job description that are missing in your resume.
-   **Interactive Resume Updater:** Allows you to add the missing keywords to your resume's skills section.
-   **PDF Generation:** Generates a new, optimized PDF of your resume.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd interactive-ai-resume-optimizer
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Once the setup is complete, you can run the Streamlit application with the following command:

```bash
streamlit run app/main.py
```

The application will be accessible in your web browser at `http://localhost:8501`.

## Project Structure

-   `app/main.py`: The main entry point for the Streamlit application.
-   `src/`: Contains the core NLP and backend logic, separated into modules.
-   `data/`: Intended for sample resumes and job descriptions.
-   `tests/`: Contains unit tests for the project.
-   `requirements.txt`: A list of the Python dependencies for the project.
-   `.gitignore`: Specifies which files and directories to ignore in version control.
