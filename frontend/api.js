const API_BASE_URL = "https://binaryduo.onrender.com";


// ==========================================
// START AGENT
// ==========================================

async function startApplicationAgent(
    resumeFile,
    jobUrl,
    targetRole
) {

    const formData = new FormData();

    formData.append(
        "resume",
        resumeFile
    );

    formData.append(
        "job_url",
        jobUrl
    );

    formData.append(
        "target_role",
        targetRole
    );


    const response = await fetch(
        `${API_BASE_URL}/start-agent`,
        {
            method: "POST",
            body: formData
        }
    );


    const data = await response.json();


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Unable to start application agent."
        );

    }


    return data;
}


// ==========================================
// GET STATUS
// ==========================================

async function getAgentStatus(
    runId
) {

    const response = await fetch(
        `${API_BASE_URL}/agent-status/${runId}`
    );


    if (!response.ok) {

        throw new Error(
            "Unable to get agent status."
        );

    }


    return await response.json();
}


// ==========================================
// GET RESULT
// ==========================================

async function getApplicationResult(
    runId
) {

    const response = await fetch(
        `${API_BASE_URL}/application-result/${runId}`
    );


    if (!response.ok) {

        throw new Error(
            "Unable to get application result."
        );

    }


    return await response.json();
}


// ==========================================
// DOWNLOAD RESUME
// ==========================================

function getResumeDownloadUrl(
    runId
) {

    return (
        `${API_BASE_URL}` +
        `/download-resume/${runId}`
    );

}


// ==========================================
// DOWNLOAD REPORT
// ==========================================

function getReportDownloadUrl(
    runId
) {

    return (
        `${API_BASE_URL}` +
        `/download-report/${runId}`
    );

}