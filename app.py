import streamlit as st
from pypdf import PdfReader
import time

st.success("Analysis Completed!")
st.set_page_config(page_title="AI Resume Analyzer")

st.title("📄 AI Resume Analyzer")

resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.file_uploader(
    "Upload Job Description",
    type=["txt"]
)

if job_description:
    st.success("Job Description uploaded successfully!")
if resume:

    reader = PdfReader(resume)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.success("Resume uploaded successfully!")

    st.text_area(
        "Resume Text",
        text,
        height=300
    )
if st.button("Analyze Resume"):

    with st.spinner("Analyzing Resume..."):

        result = analyze_resume(
            resume_text,
            job_description
        )

    st.success("Analysis Complete!")