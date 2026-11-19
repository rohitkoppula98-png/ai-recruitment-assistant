
import streamlit as st
from pypdf import PdfReader
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="👔",
    layout="wide"
)

st.title("👔 AI Recruitment Assistant")
st.caption("AI-powered candidate screening and recruitment decision support")
st.divider()

uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Job Description",
    height=180,
    placeholder="Paste the job requirements here..."
)

if st.button("Analyse & Compare Candidates", type="primary"):

    if not api_key:
        st.error("API key not found. Check your .env file.")

    elif not uploaded_files:
        st.warning("Please upload at least one resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        client = anthropic.Anthropic(api_key=api_key)
        results = []

        with st.spinner("Analysing candidate resumes..."):

            for uploaded_file in uploaded_files:

                try:
                    pdf_reader = PdfReader(uploaded_file)
                    resume_text = ""

                    for page in pdf_reader.pages:
                        resume_text += page.extract_text() or ""

                    if not resume_text.strip():
                        st.warning(
                            f"No readable text found in {uploaded_file.name}"
                        )
                        continue

                    response = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1200,
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
                                Evaluate this resume against the job description.

                                Return ONLY valid JSON:
                                {{
                                    "candidate_name": "Name",
                                    "score": 75,
                                    "experience": "Relevant experience",
                                    "matching_skills": ["Python", "SQL"],
                                    "missing_skills": ["AWS"],
                                    "assessment": "Overall assessment"
                                }}

                                Score must be an integer from 0 to 100.
                                Use only job-related evidence.
                                Do not infer protected personal characteristics.
                                Scores are advisory, not final hiring decisions.
                                If information is unavailable, say so.

                                RESUME:
                                {resume_text}

                                JOB DESCRIPTION:
                                {job_description}
                                """
                            }
                        ]
                    )

                    response_text = response.content[0].text.strip()
                    response_text = response_text.replace(
                        "```json", ""
                    ).replace("```", "").strip()

                    candidate_data = json.loads(response_text)

                    candidate_name = str(
                        candidate_data.get("candidate_name", "")
                    ).strip()

                    if not candidate_name or candidate_name.lower() == "name":
                        candidate_name = uploaded_file.name

                    raw_score = candidate_data.get("score", 0)

                    if isinstance(raw_score, bool):
                        raise ValueError("Invalid candidate score.")

                    score = int(raw_score)

                    if not 0 <= score <= 100:
                        raise ValueError("Score must be between 0 and 100.")

                    matching_skills = candidate_data.get(
                        "matching_skills", []
                    )
                    missing_skills = candidate_data.get(
                        "missing_skills", []
                    )

                    if not isinstance(matching_skills, list):
                        matching_skills = []

                    if not isinstance(missing_skills, list):
                        missing_skills = []

                    results.append({
                        "candidate_name": candidate_name,
                        "score": score,
                        "experience": candidate_data.get(
                            "experience", "Not provided"
                        ),
                        "matching_skills": matching_skills,
                        "missing_skills": missing_skills,
                        "assessment": candidate_data.get(
                            "assessment", "No assessment provided."
                        ),
                        "file_name": uploaded_file.name
                    })

                except Exception as e:
                    st.error(
                        f"Could not process {uploaded_file.name}: {e}"
                    )

        if results:

            st.divider()
            st.header("Recruitment Dashboard")

            col1, col2, col3 = st.columns(3)

            average_score = sum(
                candidate["score"] for candidate in results
            ) / len(results)

            highest_score = max(
                candidate["score"] for candidate in results
            )

            col1.metric("Candidates Analysed", len(results))
            col2.metric("Average Match Score", f"{average_score:.1f}%")
            col3.metric("Highest Match", f"{highest_score}%")

            st.subheader("Candidate Comparison")

            st.dataframe(
                [
                    {
                        "Candidate": candidate["candidate_name"],
                        "Match Score": f"{candidate['score']}%",
                        "Experience": candidate["experience"],
                        "Matching Skills": ", ".join(
                            candidate["matching_skills"]
                        ),
                        "Missing Skills": ", ".join(
                            candidate["missing_skills"]
                        )
                    }
                    for candidate in results
                ],
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Individual Candidate Assessments")

            for candidate in results:

                with st.expander(
                    f"{candidate['candidate_name']} — {candidate['score']}% Match"
                ):
                    st.write("**Resume File:**", candidate["file_name"])
                    st.write("**Experience:**", candidate["experience"])
                    st.write(
                        "**Matching Skills:**",
                        ", ".join(candidate["matching_skills"])
                    )
                    st.write(
                        "**Missing Skills:**",
                        ", ".join(candidate["missing_skills"])
                    )
                    st.write("**Assessment:**", candidate["assessment"])

            st.caption(
                "AI-generated scores are indicative decision-support estimates. "
                "Human review is required for hiring decisions."
            )
