from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

import os
import uuid
import shutil


from agent.workflow import (
    start_agent,
    get_status,
    get_result
)


app = FastAPI(
    title="Autonomous Resume & Application Agent",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# FOLDERS
# ==========================================

UPLOAD_FOLDER = "uploads"

RESUME_FOLDER = os.path.join(
    "outputs",
    "resumes"
)

REPORT_FOLDER = os.path.join(
    "outputs",
    "reports"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    RESUME_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {

        "message":
            "Autonomous Resume & Application Agent Backend",

        "status":
            "running"

    }


# ==========================================
# START AGENT
# ==========================================

@app.post("/start-agent")
async def start_application_agent(

    resume: UploadFile = File(...),

    job_url: str = Form(...),

    target_role: str = Form(...)

):

    # ======================================
    # Validate file
    # ======================================

    filename = resume.filename.lower()


    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):

        return {

            "error":
                "Only PDF and DOCX files are allowed."

        }


    # ======================================
    # Create run ID
    # ======================================

    run_id = str(
        uuid.uuid4()
    )


    # ======================================
    # Save resume
    # ======================================

    safe_filename = (
        f"{run_id}_"
        f"{resume.filename}"
    )


    file_path = os.path.join(
        UPLOAD_FOLDER,
        safe_filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )


    # ======================================
    # Start agent
    # ======================================

    start_agent(
        run_id,
        file_path,
        job_url,
        target_role
    )


    return {

        "run_id":
            run_id,

        "status":
            "started",

        "message":
            "Application agent started."

    }


# ==========================================
# AGENT STATUS
# ==========================================

@app.get(
    "/agent-status/{run_id}"
)
async def agent_status(
    run_id: str
):

    return get_status(
        run_id
    )


# ==========================================
# FINAL RESULT
# ==========================================

@app.get(
    "/application-result/{run_id}"
)
async def application_result(
    run_id: str
):

    return get_result(
        run_id
    )


# ==========================================
# DOWNLOAD RESUME
# ==========================================

@app.get(
    "/download-resume/{run_id}"
)
async def download_resume(
    run_id: str
):

    file_path = os.path.join(
        RESUME_FOLDER,
        f"{run_id}_tailored_resume.pdf"
    )


    if not os.path.exists(file_path):

        return {
            "error":
                "Resume not found."
        }


    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="tailored_resume.pdf"
    )


# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.get(
    "/download-report/{run_id}"
)
async def download_report(
    run_id: str
):

    file_path = os.path.join(
        REPORT_FOLDER,
        f"{run_id}_evidence_report.pdf"
    )


    if not os.path.exists(file_path):

        return {
            "error":
                "Report not found."
        }


    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="evidence_change_report.pdf"
    )