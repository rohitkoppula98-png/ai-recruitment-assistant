
# AI Recruitment Assistant

An AI-powered recruitment application built with Python, Streamlit and Claude API.

## Features

- Upload multiple candidate resumes in PDF format.
- Extract resume text using PyPDF.
- Analyse candidate education, experience and skills.
- Compare resumes against job descriptions.
- Generate indicative candidate suitability scores.
- Identify matching and missing skills.
- Display candidate comparisons in an HR dashboard.
- Generate individual candidate assessments.

## Technology Stack

- Python
- Streamlit
- Anthropic Claude API
- PyPDF
- Python-dotenv

## Application Workflow

1. HR uploads candidate resumes.
2. The application extracts resume text.
3. HR enters a job description.
4. Claude analyses each candidate against the requirements.
5. The application displays scores, skills and assessments.
6. HR reviews the comparison dashboard.

## Installation

1. Clone the repository.
2. Create a virtual environment:

   `python -m venv .venv`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file and add:

   `ANTHROPIC_API_KEY=your_api_key`

5. Run the application:

   `streamlit run app.py`

## Important Notes

- An Anthropic API key is required.
- API usage may incur charges.
- Suitability scores are indicative AI-generated estimates.
- Human review is required for all hiring decisions.
- Resume analysis depends on readable PDF text; scanned PDFs may require OCR.
- The application is a prototype, not a production hiring system.
