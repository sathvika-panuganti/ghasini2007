# 🤖 Autonomous Resume & Application Agent

An AI-powered application assistant that analyzes a candidate's resume and a target job description to create a tailored, evidence-based resume.

Instead of simply generating a resume once, the system evaluates its output, identifies weaknesses, and can replan and revise the application when needed.

## 🚀 Live Demo

- **Frontend:** https://ghasini2007.vercel.app/
- **Backend API:** https://binaryduo.onrender.com/

## 📸 Application Preview

### Agent Activity & Decision Engine

The application provides a live view of what the agent is currently doing, why it made a decision, and what action it plans to take next.

<img width="1130" height="712" alt="image" src="https://github.com/user-attachments/assets/b1a75c54-f654-4211-9ffb-822e3037b6de" />


The dashboard tracks the application workflow from resume parsing and job analysis to evidence matching, evaluation, replanning, and final verification.

## ✨ Features

- 📄 Parse resumes from PDF and DOCX files
- 💼 Analyze real job descriptions
- 🔍 Match job requirements with candidate evidence
- 🤖 Generate role-specific resumes using AI
- 📊 Evaluate ATS alignment, relevance, and evidence coverage
- 🔄 Replan and revise when the generated resume has weaknesses
- 🛡️ Keep resume changes grounded in verified candidate information
- 📑 Generate a formatted PDF resume
- 📝 Track application decisions and changes
- ✅ Perform final factual verification

## 🔄 How It Works

1. **Analyze**  
   Parse the candidate's resume and target job description.

2. **Match**  
   Identify relevant skills, experience, projects, and supporting evidence.

3. **Decide**  
   The agent determines what action should be taken next based on the current application state.

4. **Generate**  
   Create a tailored resume using verified candidate information.

5. **Evaluate**  
   Check the resume for ATS alignment, job relevance, evidence coverage, and factual consistency.

6. **Replan**  
   If weaknesses are detected, the agent changes its plan and performs another revision.

7. **Verify**  
   Validate the final application before generating the final output.

## 🧠 Agent Behavior

The system is designed as a **decision loop rather than a fixed generation pipeline**.

The agent maintains application state and repeatedly follows:

**Observe → Decide → Act → Evaluate → Replan → Verify**

For example, if the generated resume has strong evidence coverage but weak relevance to the target role, the agent can prioritize improving job alignment instead of blindly regenerating the entire resume.

The agent also follows an important constraint:

> **No evidence = no claim.**

Missing skills, experience, projects, or credentials are not fabricated simply to improve keyword matching.

## 🏗️ Architecture

### Frontend

- HTML5
- CSS3
- JavaScript (ES6+)
- REST API integration
- Application activity timeline
- Agent decision display
- Evaluation results
- Resume preview and change reporting

### Backend

- Python
- FastAPI
- Pydantic
- Agent Controller
- State Management
- Decision Planner
- OpenAI API

### Document & Web Processing

- PyPDF
- python-docx
- Requests
- BeautifulSoup
- ReportLab

### Agent Tools

- Resume Parser
- Job Description Analyzer
- Evidence Matcher
- Job Researcher
- Resume Generator
- ATS Evaluator
- Fact Checker
- PDF Renderer
- Final Verifier

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and agent logic |
| FastAPI | Backend REST API |
| JavaScript | Frontend logic and API communication |
| HTML5 / CSS3 | Frontend interface |
| OpenAI API | AI reasoning and resume generation |
| Pydantic | Data validation and state models |
| PyPDF | Resume PDF parsing |
| python-docx | DOCX parsing |
| BeautifulSoup | Job page parsing |
| Requests | Web requests |
| ReportLab | PDF generation |


├── requirements.txt
└── README.md
