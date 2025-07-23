
import streamlit as st
import openai
import pdfplumber
from docx import Document
from io import BytesIO
from utils import extract_text, generate_docx

st.set_page_config(page_title="Resume Tailor Pro", layout="wide")
st.title("🧠 Resume Tailor Pro")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def tailor_resume(resume_text, job_description):
    prompt = f"""
You are an expert resume writer.

Given the following base resume:
{resume_text}

And this job description:
{job_description}

Rewrite the summary and experience sections of the resume to match the job description using relevant keywords, while keeping it human and ATS-friendly. Keep formatting professional.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

resume_file = st.file_uploader("📄 Upload Your Resume (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
job_description = st.text_area("📝 Paste the Job Description", height=300)

if st.button("✍️ Tailor My Resume"):
    if resume_file and job_description:
        resume_text = extract_text(resume_file)
        with st.spinner("Tailoring resume..."):
            tailored_resume = tailor_resume(resume_text, job_description)
            output_docx = generate_docx(tailored_resume)
        st.success("✅ Done! Your resume is tailored.")
        st.download_button("📥 Download as Word (.docx)", data=output_docx, file_name="Tailored_Resume.docx")
        st.text_area("🎯 Preview", tailored_resume, height=400)
    else:
        st.warning("Please upload a resume and paste a job description.")
