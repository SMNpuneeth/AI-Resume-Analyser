import streamlit as st
import pdfplumber
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================================
# Page config
# ============================================
st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="📄"
)

st.title("📄 AI Resume Analyser")
st.caption("Upload your resume and paste a job description — get instant AI feedback.")

# ============================================
# Extract text from PDF
# ============================================
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

# ============================================
# Analyse resume against JD
# ============================================
def analyse_resume(resume_text, job_description):
    prompt = f"""
    You are an elite HR director with 20 years of experience at 
    Fortune 500 companies. You have reviewed over 50,000 resumes 
    and conducted thousands of technical interviews. You understand 
    exactly what separates candidates who get hired from those who 
    get rejected.

    Your job is to analyse the resume against the job description 
    with zero bias and maximum accuracy.

    STRICT SCORING RULES — follow mathematically, no exceptions:
    - List every unique technical keyword and requirement in the JD
    - Count exactly how many appear in the resume
    - match_score = (matched keywords / total keywords) * 100
    - Subtract 8 points for each critical requirement missing
    - Subtract 3 points for each preferred requirement missing  
    - Never give above 95 — no resume is perfect
    - Never inflate — a weak resume must get a low score
    - Round to nearest whole number

    ATS SCORING RULES:
    - Check for standard section headers: Skills, Experience, Education, Projects
    - Check for quantified achievements (numbers, percentages, metrics)
    - Check for keyword density matching the JD
    - Check for clean formatting indicators (no tables, no graphics mentioned)
    - ats_score = weighted average of above checks

    ROLE SUITABILITY RULES:
    - Junior: 0-2 years experience, fresher projects, entry level skills
    - Mid: 2-5 years experience, production projects, some leadership
    - Senior: 5+ years, team leadership, architecture decisions, mentoring
    - Be realistic — most freshers are Junior regardless of skills listed

    Return ONLY a raw JSON object with exactly these keys and nothing else:
    {{
        "match_score": <integer 0-95>,
        "ats_score": <integer 0-100>,
        "role_suitability": <"Junior" or "Mid" or "Senior">,
        "missing_keywords": [<list of strings>],
        "strengths": [<list of strings — be specific, mention actual content from resume>],
        "weaknesses": [<list of strings — be honest and direct>],
        "suggestions": [<list of strings — each suggestion must be a specific actionable line to add or change>],
        "interview_questions": [<list of exactly 5 strings — likely interview questions based on this specific resume and JD>],
        "jd_compatibility": <exactly one of: "Good Fit", "Stretch Role", or "Out of Range" — compare the candidate level from role_suitability against the seniority level required by the JD>
    }}

    No markdown. No explanation. No extra text. Raw JSON only.
    Start your response with {{ and end with }}

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    return result

# ============================================
# Score colour — green, orange, or red
# ============================================
def get_score_color(score):
    if score >= 70:
        return "green"
    elif score >= 40:
        return "orange"
    else:
        return "red"

# ============================================
# Sidebar instructions
# ============================================
with st.sidebar:
    st.header("📋 How to use")
    st.write("1. Upload your resume as a PDF")
    st.write("2. Paste the job description")
    st.write("3. Click Analyse")
    st.write("4. Get instant AI feedback")
    st.divider()
    st.subheader("📊 Score guide")
    st.write("🟢 70%+ — Strong match")
    st.write("🟡 40–69% — Decent match")
    st.write("🔴 Below 40% — Needs work")
    st.divider()
    st.caption("Your resume is never stored. Analysis happens in real time.")

# ============================================
# Main UI — two columns
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📎 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

with col2:
    st.subheader("📝 Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        height=200,
        placeholder="We are looking for an AI Engineer with experience in Python, LangChain, RAG..."
    )

st.divider()

# ============================================
# Analyse button
# ============================================
analyse_btn = st.button("🔍 Analyse Resume", use_container_width=True)

if analyse_btn:
    if not uploaded_file:
        st.warning("Please upload your resume first.")
    elif not job_description.strip():
        st.warning("Please paste the job description first.")
    else:
        with st.spinner("Analysing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyse_resume(resume_text, job_description)

        st.success("Analysis complete!")
        st.divider()

        # ============================================
        # Match score — big and bold
        # ============================================
        score = result["match_score"]
        color = get_score_color(score)

        st.markdown(f"## Match Score")
        st.markdown(
            f"<h1 style='color:{color}; font-size:72px'>{score}%</h1>",
            unsafe_allow_html=True
        )

        if score >= 70:
            st.success("Strong match. You are a solid candidate for this role.")
        elif score >= 40:
            st.warning("Decent match. A few improvements will strengthen your application.")
        else:
            st.error("Low match. Significant gaps between your resume and this role.")

        st.divider()



        # Two columns for ATS score and Role suitability
        a1, a2 = st.columns(2)

        with a1:
            ats = result["ats_score"]
            ats_color = get_score_color(ats)
            st.markdown("### 📊 ATS Score")
            st.markdown(
                f"<h2 style='color:{ats_color}'>{ats}%</h2>",
                unsafe_allow_html=True
            )
            st.caption("How well your resume passes Applicant Tracking Systems")
            if ats >= 70:
                st.success("ATS friendly — recruiters will see your resume")
            elif ats >= 40:
                st.warning("Partially ATS friendly — add more keywords")
            else:
                st.error("Poor ATS score — resume may get filtered out automatically")

        with a2:
            suitability = result["role_suitability"]
            st.markdown("### 🎯 Role Suitability")

            if suitability == "Junior":
                st.markdown("<h2 style='color:green'>🟢 Junior</h2>", unsafe_allow_html=True)
                st.success("Good fit for this role as a fresher or junior candidate")
            elif suitability == "Mid":
                st.markdown("<h2 style='color:orange'>🟡 Mid Level</h2>", unsafe_allow_html=True)
                st.warning("You meet some requirements but may need more experience")
            else:
                st.markdown("<h2 style='color:red'>🔴 Senior Level</h2>", unsafe_allow_html=True)
                st.info("This resume reflects senior level experience.")

        st.divider()
        
        st.markdown("### 🎯 JD Compatibility")

        compatibility = result["jd_compatibility"]

        if compatibility == "Good Fit":
            st.success("✅ This job description matches your current level. Apply confidently.")

        elif compatibility == "Stretch Role":
            st.warning("⚠️ This role is slightly above your current level. Possible but will need strong preparation.")

        else:
            st.error("🚫 This role requires significantly more experience than your resume shows. Consider applying for junior roles first and using this analysis to know what to build toward.")


        # ============================================
        # Results in 3 columns
        # ============================================
        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown("### ✅ Strengths")
            for strength in result["strengths"]:
                st.write(f"• {strength}")

        with r2:
            st.markdown("### ❌ Weaknesses")
            for weakness in result["weaknesses"]:
                st.write(f"• {weakness}")

        with r3:
            st.markdown("### 🔑 Missing Keywords")
            for keyword in result["missing_keywords"]:
                st.write(f"• {keyword}")

        st.divider()

        # ============================================
        # Suggestions — full width
        # ============================================
        st.markdown("### 💡 Suggestions to improve your resume")
        for i, suggestion in enumerate(result["suggestions"]):
            st.info(f"**{i+1}.** {suggestion}")

        st.divider()

        # ============================================
        # Interview questions
        # ============================================
        st.markdown("### 🎤 Likely Interview Questions")
        st.caption("Based on your resume and this job description — prepare answers for these.")

        for i, question in enumerate(result["interview_questions"]):
            with st.expander(f"Question {i+1}: {question}"):
                st.write("💡 Prepare a structured answer using the STAR method:")
                st.write("**S**ituation — set the context")
                st.write("**T**ask — what was your responsibility")
                st.write("**A**ction — what did you do specifically")
                st.write("**R**esult — what was the outcome")

        st.divider()

        # ============================================
        # Download result as text
        # ============================================

        report = f"""
        RESUME ANALYSIS REPORT
        ======================

        Match Score  : {result['match_score']}%
        ATS Score    : {result['ats_score']}%
        Suitability  : {result['role_suitability']} Level

        STRENGTHS:
        {chr(10).join(f'- {s}' for s in result['strengths'])}

        WEAKNESSES:
        {chr(10).join(f'- {w}' for w in result['weaknesses'])}

        MISSING KEYWORDS:
        {chr(10).join(f'- {k}' for k in result['missing_keywords'])}

        LIKELY INTERVIEW QUESTIONS:
        {chr(10).join(f'{i+1}. {q}' for i, q in enumerate(result['interview_questions']))}

        SUGGESTIONS:
        {chr(10).join(f'{i+1}. {s}' for i, s in enumerate(result['suggestions']))}
        """

        st.download_button(
            label="📥 Download Analysis Report",
            data=report,
            file_name="resume_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )