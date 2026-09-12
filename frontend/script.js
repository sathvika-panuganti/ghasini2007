// ==========================================
// ELEMENTS
// ==========================================

const inputScreen =
    document.getElementById("inputScreen");

const agentScreen =
    document.getElementById("agentScreen");

const resultScreen =
    document.getElementById("resultScreen");


const resumeFile =
    document.getElementById("resumeFile");

const uploadBox =
    document.getElementById("uploadBox");

const fileStatus =
    document.getElementById("fileStatus");


const jobUrl =
    document.getElementById("jobUrl");

const targetRole =
    document.getElementById("targetRole");


const startButton =
    document.getElementById("startButton");


// ==========================================
// RESUME SELECTION
// ==========================================

resumeFile.addEventListener(
    "change",
    function () {

        const file =
            resumeFile.files[0];


        if (!file) {

            return;

        }


        validateFile(file);

    }
);


// ==========================================
// FILE VALIDATION
// ==========================================

function validateFile(file) {

    const extension =
        file.name
            .split(".")
            .pop()
            .toLowerCase();


    if (
        extension !== "pdf"
        &&
        extension !== "docx"
    ) {

        fileStatus.textContent =
            "Please select a PDF or DOCX file.";

        fileStatus.style.color =
            "#c0392b";

        resumeFile.value = "";

        return false;

    }


    fileStatus.textContent =
        "✓ " + file.name + " selected";

    fileStatus.style.color =
        "#27834a";


    return true;
}


// ==========================================
// DRAG AND DROP
// ==========================================

uploadBox.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        uploadBox.style.borderColor =
            "#555b65";

    }
);


uploadBox.addEventListener(
    "dragleave",
    function () {

        uploadBox.style.borderColor =
            "#cdd2d8";

    }
);


uploadBox.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        uploadBox.style.borderColor =
            "#cdd2d8";


        const file =
            event.dataTransfer.files[0];


        if (!file) {

            return;

        }


        const valid =
            validateFile(file);


        if (!valid) {

            return;

        }


        const dataTransfer =
            new DataTransfer();


        dataTransfer.items.add(file);


        resumeFile.files =
            dataTransfer.files;

    }
);


// ==========================================
// START APPLICATION
// ==========================================

startButton.addEventListener(
    "click",
    async function () {

        const file =
            resumeFile.files[0];

        const url =
            jobUrl.value.trim();

        const role =
            targetRole.value.trim();


        if (!file) {

            alert(
                "Please upload your resume."
            );

            return;

        }


        if (!url) {

            alert(
                "Please enter the job posting URL."
            );

            return;

        }


        if (!role) {

            alert(
                "Please enter the target role."
            );

            return;

        }


        // ==================================
        // SHOW AGENT SCREEN
        // ==================================

        inputScreen.classList.add(
            "hidden"
        );

        agentScreen.classList.remove(
            "hidden"
        );


        startButton.disabled = true;


        try {

            // ==================================
            // START REAL BACKEND AGENT
            // ==================================

            const response =
                await startApplicationAgent(
                    file,
                    url,
                    role
                );


            const runId =
                response.run_id;


            monitorAgent(runId);

        }
        catch (error) {

            alert(
                error.message
            );


            startButton.disabled =
                false;

        }

    }
);


// ==========================================
// MONITOR AGENT
// ==========================================

async function monitorAgent(
    runId
) {

    const interval =
        setInterval(
            async function () {

                try {

                    const status =
                        await getAgentStatus(
                            runId
                        );


                    updateFrontend(
                        status
                    );


                    if (
                        status.status ===
                        "completed"
                    ) {

                        clearInterval(
                            interval
                        );


                        const result =
                            await getApplicationResult(
                                runId
                            );


                        showBackendResults(
                            result,
                            runId
                        );

                    }


                    if (
                        status.status ===
                        "failed"
                    ) {

                        clearInterval(
                            interval
                        );


                        alert(
                            "Agent failed: " +
                            (
                                status.error ||
                                "Unknown error"
                            )
                        );

                    }

                }
                catch (error) {

                    console.log(
                        error
                    );

                }

            },
            1200
        );

}


// ==========================================
// UPDATE TIMELINE
// ==========================================

function updateFrontend(
    status
) {

    const timelineItems =
        document.querySelectorAll(
            ".timeline-item"
        );


    const stepNames = [

        "Resume parsed",

        "Candidate information extracted",

        "Job posting checked",

        "Job requirements identified",

        "Relevant experience matched",

        "Resume prepared",

        "Application evaluated",

        "Application needs revision",

        "Information checked",

        "Final application verified"

    ];


    const currentStep =
        status.current_step;


    timelineItems.forEach(
        function (item, index) {

            const title =
                item.querySelector(
                    "strong"
                );

            const text =
                item.querySelector(
                    "p"
                );


            if (!title || !text) {

                return;

            }


            if (
                title.textContent.trim()
                ===
                currentStep
            ) {

                item.classList.remove(
                    "pending"
                );

                item.classList.add(
                    "running"
                );


                text.textContent =
                    "In progress";

            }

        }
    );


    // ======================================
    // REPLAN
    // ======================================

    const replan =
        document.querySelector(
            ".timeline-item.replan"
        );


    if (
        status.decision ===
        "REPLAN"
    ) {

        replan.classList.remove(
            "pending"
        );

        replan.classList.add(
            "running"
        );

        replan.querySelector(
            "p"
        ).textContent =
            "Agent decided to revise application";

    }


    // ======================================
    // DECISION PANEL
    // ======================================

    document.getElementById(
        "decision"
    ).textContent =
        status.decision || "Working";


    document.getElementById(
        "decisionReason"
    ).textContent =
        status.reason || "";


    document.getElementById(
        "decisionAction"
    ).textContent =
        status.action || "";


    // ======================================
    // STATUS
    // ======================================

    const executionStatus =
        document.getElementById(
            "executionStatus"
        );


    if (
        status.status ===
        "running"
    ) {

        executionStatus.textContent =
            "In progress";

    }

}


// ==========================================
// SHOW RESULTS
// ==========================================

function showBackendResults(
    result,
    runId
) {

    agentScreen.classList.add(
        "hidden"
    );

    resultScreen.classList.remove(
        "hidden"
    );


    const evaluation =
        result.evaluation;


    document.getElementById(
        "atsScore"
    ).textContent =
        evaluation.ats_score + "%";


    document.getElementById(
        "relevanceScore"
    ).textContent =
        evaluation.relevance_score + "%";


    document.getElementById(
        "evidenceScore"
    ).textContent =
        evaluation.evidence_score + "%";


    document.getElementById(
        "factCheck"
    ).textContent =
        evaluation.factual_consistency;


    document.getElementById(
        "formatCheck"
    ).textContent =
        evaluation.formatting;


    document.getElementById(
        "resumeFilename"
    ).textContent =
        result.resume_filename;


    // ======================================
    // DOWNLOAD BUTTON
    // ======================================

    document.getElementById(
        "downloadResume"
    ).onclick =
        function () {

            window.open(
                getResumeDownloadUrl(
                    runId
                ),
                "_blank"
            );

        };


    // ======================================
    // REPORT
    // ======================================

    document.getElementById(
        "downloadReport"
    ).onclick =
        function () {

            window.open(
                getReportDownloadUrl(
                    runId
                ),
                "_blank"
            );

        };


    document.getElementById(
        "viewReport"
    ).onclick =
        function () {

            window.open(
                getReportDownloadUrl(
                    runId
                ),
                "_blank"
            );

        };

}


// ==========================================
// WAIT
// ==========================================

function wait(milliseconds) {

    return new Promise(
        function (resolve) {

            setTimeout(
                resolve,
                milliseconds
            );

        }
    );

}