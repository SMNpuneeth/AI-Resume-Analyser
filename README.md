# 📄 AI Resume Analyser

> Upload your resume. Paste a job description. Get honest AI feedback in seconds — match score, ATS score, role suitability, JD compatibility, and likely interview questions.

---

## ✨ What it does

Most people don't know why their resume gets rejected. This tool tells you exactly why — with numbers, not guesses.

The AI reads your resume against a real job description and gives you a full breakdown. No hallucination. No inflated scores. Just honest analysis.

---

## 🎯 Features

- 📊 **Match Score** — strict keyword-based calculation of how well your resume fits the JD
- 🤖 **ATS Score** — how well your resume passes Applicant Tracking Systems before a human sees it
- 🎯 **Role Suitability** — Junior, Mid, or Senior verdict based on your actual resume content
- 🔗 **JD Compatibility** — tells you honestly if this job is realistic for your current level
- ✅ **Strengths** — what you have that the JD wants
- ❌ **Weaknesses** — honest gaps between your resume and the role
- 🔑 **Missing Keywords** — exactly what to add to your resume
- 💡 **Suggestions** — specific actionable lines to improve your resume
- 🎤 **Interview Questions** — 5 likely questions based on YOUR resume and THIS JD with STAR method guidance
- 📥 **Download Report** — full analysis as a text file

---

## 🧠 How it works

```
Upload Resume (PDF) + Paste Job Description
            ↓
pdfplumber extracts text from PDF
            ↓
LLaMA 3.3 analyses both with strict scoring rules
            ↓
Returns structured JSON with all 9 analysis points
            ↓
Streamlit displays everything cleanly
            ↓
Download full report
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core language |
| **Streamlit** | Web UI |
| **Groq API + LLaMA 3.3** | AI analysis engine (free) |
| **pdfplumber** | PDF text extraction |
| **python-dotenv** | Secure API key management |

---

## 📁 Project Structure

```
resume-analyser/
├── app.py                  ← main Streamlit application
├── requirements.txt        ← Python dependencies
├── .env                    ← your API key (create this yourself)
└── .gitignore              ← keeps secrets off GitHub
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/SMNpuneeth/AI-Resume-Analyser.git
cd AI-Resume-Analyser
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Get your free Groq API key
Go to console.groq.com → sign up free → create an API key

### 4️⃣ Create your .env file
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Run the app
```bash
python -m streamlit run app.py
```

Open browser at http://localhost:8501

---

## 📊 Score Guide

| Score | Meaning |
|---|---|
| 🟢 70%+ | Strong match — apply now |
| 🟡 40–69% | Decent match — improve resume first |
| 🔴 Below 40% | Significant gaps — build more skills |

| JD Compatibility | Meaning |
|---|---|
| ✅ Good Fit | This role matches your level |
| ⚠️ Stretch Role | Slightly above your level — possible with prep |
| 🚫 Out of Range | Significantly above your level — build toward it |

---

## 💬 Example Output

```
Match Score     : 67%
ATS Score       : 72%
Role Suitability: Junior
JD Compatibility: Stretch Role

Strengths       : Python, FastAPI, REST APIs, PostgreSQL
Missing Keywords: LangChain, RAG, ChromaDB, Vector databases
Weaknesses      : No production AI experience, no LLM projects

Interview Questions:
1. Walk me through a project where you used Python for backend development
2. How would you approach building a RAG pipeline from scratch?
3. What do you know about vector databases and embeddings?
4. How do you handle API rate limiting in production?
5. Where do you see AI engineering heading in the next 2 years?
```

---

## 🚀 What I Learned Building This

- Structured JSON output from LLMs using strict prompting
- How ATS systems work and what they filter
- PDF text extraction with pdfplumber
- Building multi-section Streamlit UIs with columns and expanders
- Prompt engineering for consistent, accurate, non-inflated scoring
- Temperature 0 for deterministic AI responses

---

## 🔮 Future Improvements

- [ ] Support for DOCX resume format
- [ ] Side by side resume vs JD keyword visualisation
- [ ] Save and compare multiple analyses
- [ ] Deploy to Streamlit Cloud for public access
- [ ] Email the report directly to the user

---

## 👨‍💻 Author

**Puneeth Sai**
AI Engineer (Fresher) — building real AI tools from scratch

GitHub: https://github.com/SMNpuneeth

---

*Built with Python + LLaMA 3.3 by Puneeth Sai*
