# 🤖 Autonomous Resume & Application Agent

An AI-powered application assistant that analyzes a candidate's resume and a target job description to create a tailored, evidence-based resume.

The system evaluates the generated resume and can revise it when important areas such as relevance, ATS alignment, or evidence coverage need improvement.

## ✨ Features

* 📄 Parse resumes from PDF and DOCX files
* 💼 Analyze job descriptions
* 🔍 Match job requirements with candidate experience
* 🤖 AI-assisted resume generation
* 📊 ATS and relevance evaluation
* 🔄 Evaluation-driven resume revision
* 🛡️ Evidence-based generation to reduce fabricated claims
* 📑 Generate a final PDF resume
* 📝 Provide a report explaining important changes

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **OpenAI API**
* **Pydantic**
* **PyPDF**
* **python-docx**
* **ReportLab**
* **BeautifulSoup**
* **Requests**

🔄 How it works
Analyze — Parse the resume and job description.
Match — Identify relevant candidate experience and skills.
Generate — Create a role-specific resume using verified information.
Evaluate — Check ATS alignment, relevance, and evidence coverage.
Revise — Improve the resume when evaluation identifies weaknesses.
Verify — Fact-check the final result and generate the PDF.


## 🚀 Setup

Clone the repository:

```bash
git clone https://github.com/sathvika-panuganti/ghasini2007.git
cd ghasini2007
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```bash
uvicorn app:app --reload
```


## 📄 License

This project is for educational and development purposes.

