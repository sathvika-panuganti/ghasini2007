import os
import threading
import time

from agent.resume_parser import parse_resume
from agent.job_analyzer import fetch_job_description
from agent.evidence_extractor import extract_evidence
from agent.matcher import extract_job_requirements, match_evidence
from agent.resume_generator import generate_resume
from agent.evaluator import evaluate_application
from agent.verifier import verify_application
from agent.report_generator import generate_report

from agent.llm_agent import ask_agent
from agent.agent_state import (
    create_initial_state,
    record_action,
    update_state
)


# Stores active runs
runs = {}


# ---------------------------------------------------------
# UPDATE FRONTEND STATUS
# ---------------------------------------------------------

def update_status(
    run_id,
    step,
    decision,
    reason,
    action
):
    runs[run_id].update({
        "current_step": step,
        "decision": decision,
        "reason": reason,
        "action": action
    })


# ---------------------------------------------------------
# START AGENT
# ---------------------------------------------------------

def start_agent(
    run_id,
    resume_path,
    job_url,
    target_role
):

    # Create initial persistent task state
    state = create_initial_state(
        run_id,
        target_role,
        job_url
    )

    runs[run_id] = {
        "status": "running",

        "current_step": "Starting",

        "decision": "START",

        "reason": (
            "Application goal received. "
            "Agent is preparing the task."
        ),

        "action": "Start autonomous resume analysis",

        "state": state
    }

    # Run workflow in background
    thread = threading.Thread(
        target=run_workflow,
        args=(
            run_id,
            resume_path,
            job_url,
            target_role
        )
    )

    thread.daemon = True
    thread.start()


# ---------------------------------------------------------
# MAIN AUTONOMOUS WORKFLOW
# ---------------------------------------------------------

def run_workflow(
    run_id,
    resume_path,
    job_url,
    target_role
):

    state = runs[run_id]["state"]

    try:

        # =================================================
        # STEP 1 — READ RESUME
        # =================================================

        update_status(
            run_id,
            "Resume parsed",
            "OBSERVE",
            "Resume file received.",
            "Extract candidate information from resume."
        )

        record_action(
            state,
            "Read candidate resume",
            "Resume file received from user."
        )

        resume_text = parse_resume(resume_path)

        if not resume_text:
            raise ValueError(
                "Could not extract text from resume."
            )

        update_state(
            state,
            resume_text=resume_text,
            status="resume_observed"
        )

        time.sleep(1)


        # =================================================
        # STEP 2 — EXTRACT CANDIDATE EVIDENCE
        # =================================================

        update_status(
            run_id,
            "Candidate evidence extracted",
            "REASON",
            "Resume text is available.",
            "Identify genuine skills, projects, education and experience."
        )

        evidence = extract_evidence(
            resume_text
        )

        update_state(
            state,
            candidate_evidence=evidence,
            status="evidence_observed"
        )

        record_action(
            state,
            "Extract candidate evidence",
            f"Found {len(evidence['skills'])} candidate skills."
        )

        time.sleep(1)


        # =================================================
        # STEP 3 — FETCH JOB POSTING
        # =================================================

        update_status(
            run_id,
            "Job posting checked",
            "OBSERVE",
            "Job URL was provided.",
            "Fetch and inspect the real job posting."
        )

        record_action(
            state,
            "Fetch job posting",
            f"Accessing job URL: {job_url}"
        )

        job_text = fetch_job_description(
            job_url
        )

        if not job_text:
            raise ValueError(
                "Could not extract job posting."
            )

        update_state(
            state,
            job_text=job_text,
            status="job_observed"
        )

        time.sleep(1)


        # =================================================
        # STEP 4 — IDENTIFY JOB REQUIREMENTS
        # =================================================

        update_status(
            run_id,
            "Job requirements identified",
            "REASON",
            "Job posting was successfully fetched.",
            "Identify skills and requirements needed for the role."
        )

        job_requirements = extract_job_requirements(
            job_text
        )

        update_state(
            state,
            job_requirements=job_requirements,
            status="requirements_identified"
        )

        record_action(
            state,
            "Identify job requirements",
            f"Found {len(job_requirements)} relevant requirements."
        )

        time.sleep(1)


        # =================================================
        # STEP 5 — MATCH CANDIDATE EVIDENCE
        # =================================================

        update_status(
            run_id,
            "Candidate evidence matched",
            "REASON",
            "Job requirements are available.",
            "Compare genuine candidate evidence with job requirements."
        )

        matching = match_evidence(
            evidence,
            job_requirements
        )

        update_state(
            state,
            matched_evidence=matching["matched"],
            missing_requirements=matching["missing"],
            status="evidence_matched"
        )

        record_action(
            state,
            "Match candidate evidence",
            (
                f"{len(matching['matched'])} requirements supported; "
                f"{len(matching['missing'])} requirements unsupported."
            )
        )

        time.sleep(1)


        # =================================================
        # STEP 6 — AI REASONING
        # =================================================

        update_status(
            run_id,
            "Agent is reasoning",
            "REASON",
            "Candidate evidence and job requirements are available.",
            "Use AI reasoning to decide the next action."
        )

        ai_analysis = ask_agent(
            resume_text=resume_text,
            job_text=job_text,
            target_role=target_role,
            candidate_evidence=evidence,
            job_requirements=job_requirements,
            evaluation=None
        )

        update_state(
            state,
            ai_analysis=ai_analysis,
            plan=ai_analysis.get("plan", []),
            status="ai_reasoned"
        )

        record_action(
            state,
            "AI reasoning",
            ai_analysis.get(
                "reason",
                "AI generated a plan."
            )
        )

        time.sleep(1)


        # =================================================
        # STEP 7 — PREPARE INITIAL RESUME
        # =================================================

        update_status(
            run_id,
            "Tailored resume prepared",
            "ACT",
            "Relevant candidate evidence has been identified.",
            "Create a role-specific resume using only verified evidence."
        )

        resume_output = os.path.join(
            "outputs",
            "resumes",
            f"{run_id}_tailored_resume.pdf"
        )

        generate_resume(
            resume_text,
            target_role,
            matching["matched"],
            resume_output
        )

        record_action(
            state,
            "Generate tailored resume",
            "Resume created using verified candidate evidence."
        )

        update_state(
            state,
            status="resume_generated"
        )

        time.sleep(1)


        # =================================================
        # STEP 8 — EVALUATE RESULT
        # =================================================

        update_status(
            run_id,
            "Application evaluated",
            "EVALUATE",
            "Initial tailored resume has been created.",
            "Evaluate ATS relevance and evidence coverage."
        )

        evaluation = evaluate_application(
            matching["matched"],
            matching["missing"]
        )

        update_state(
            state,
            evaluation=evaluation,
            status="evaluated"
        )

        record_action(
            state,
            "Evaluate application",
            (
                f"Evidence coverage: "
                f"{evaluation['evidence_score']}%. "
                f"Decision: {evaluation['decision']}."
            )
        )

        time.sleep(1)


        # =================================================
        # STEP 9 — AUTONOMOUS REPLANNING
        # =================================================

        replanned = False

        max_replans = state.get(
            "max_replans",
            2
        )

        while (
            evaluation["evidence_score"] < 70
            and state["replan_count"] < max_replans
        ):

            replanned = True

            state["replan_count"] += 1

            replan_number = state["replan_count"]

            update_status(
                run_id,
                "Agent is replanning",
                "REPLAN",
                (
                    "Evidence coverage is below the target. "
                    "The agent will revise its strategy without "
                    "inventing candidate information."
                ),
                (
                    f"Replan attempt {replan_number}: "
                    "emphasize stronger verified evidence."
                )
            )

            record_action(
                state,
                "REPLAN",
                (
                    f"Evidence score was "
                    f"{evaluation['evidence_score']}%. "
                    "Agent rejected unsupported claims."
                )
            )

            time.sleep(2)


            # ---------------------------------------------
            # AI REASONING FOR REPLAN
            # ---------------------------------------------

            update_status(
                run_id,
                "Replanning strategy",
                "REASON",
                "Previous plan did not meet the evaluation target.",
                "Ask AI for a safer alternative strategy."
            )

            ai_analysis = ask_agent(
                resume_text=resume_text,
                job_text=job_text,
                target_role=target_role,
                candidate_evidence=evidence,
                job_requirements=job_requirements,
                evaluation=evaluation
            )

            update_state(
                state,
                ai_analysis=ai_analysis,
                plan=ai_analysis.get(
                    "plan",
                    []
                ),
                status="replanned"
            )

            record_action(
                state,
                "Generate new plan",
                ai_analysis.get(
                    "reason",
                    "New plan generated."
                )
            )

            time.sleep(1)


            # ---------------------------------------------
            # ACT ON NEW PLAN
            # ---------------------------------------------

            update_status(
                run_id,
                "Resume revised",
                "ACT",
                (
                    "Agent created a new plan using "
                    "only verified candidate evidence."
                ),
                "Regenerate the resume using the revised strategy."
            )

            generate_resume(
                resume_text,
                target_role,
                matching["matched"],
                resume_output
            )

            record_action(
                state,
                "Revise resume",
                (
                    "Resume regenerated without adding "
                    "unsupported candidate claims."
                )
            )

            time.sleep(1)


            # ---------------------------------------------
            # OBSERVE RESULT AGAIN
            # ---------------------------------------------

            update_status(
                run_id,
                "Revised application evaluated",
                "EVALUATE",
                "The revised resume has been generated.",
                "Evaluate the revised application again."
            )

            evaluation = evaluate_application(
                matching["matched"],
                matching["missing"]
            )

            update_state(
                state,
                evaluation=evaluation,
                status="reevaluated"
            )

            record_action(
                state,
                "Observe revised result",
                (
                    f"New evidence coverage: "
                    f"{evaluation['evidence_score']}%."
                )
            )

            time.sleep(1)


        # =================================================
        # STEP 10 — FACTUAL VERIFICATION
        # =================================================

        update_status(
            run_id,
            "Checking factual consistency",
            "VERIFY",
            (
                "Resume generation and evaluation are complete."
            ),
            "Verify that generated content is supported by the original resume."
        )

        # Read the generated PDF text
        generated_resume_text = ""

        try:
            generated_resume_text = parse_resume(
                resume_output
            )
        except Exception:
            generated_resume_text = ""

        # Evidence used for verification
        matched_evidence = matching["matched"]

        verification = verify_application(
            resume_text,
            generated_resume_text,
            matched_evidence
        )

        update_state(
            state,
            verification=verification,
            status="verified"
        )

        record_action(
            state,
            "Verify factual consistency",
            verification.get(
                "message",
                "Verification completed."
            )
        )

        time.sleep(1)


        # =================================================
        # STEP 11 — FINAL DECISION
        # =================================================

        if not verification["passed"]:

            update_status(
                run_id,
                "Verification failed",
                "REPLAN",
                (
                    "The final verification detected "
                    "unsupported evidence."
                ),
                "Stop and prevent an unsafe application."
            )

            record_action(
                state,
                "Final verification failed",
                "Application package was not approved."
            )

            runs[run_id]["status"] = "failed"

            runs[run_id]["error"] = (
                "Final factual verification failed."
            )

            return


        # =================================================
        # STEP 12 — GENERATE REPORT
        # =================================================

        update_status(
            run_id,
            "Generating evidence report",
            "ACT",
            "Final application passed factual verification.",
            "Create evidence and change report."
        )

        report_output = os.path.join(
            "outputs",
            "reports",
            f"{run_id}_evidence_report.pdf"
        )

        generate_report(
            report_output,
            target_role,
            matching["matched"],
            matching["missing"],
            evaluation,
            verification
        )

        record_action(
            state,
            "Generate evidence report",
            "Evidence and evaluation report created."
        )

        time.sleep(1)


        # =================================================
        # STEP 13 — FINAL VERIFICATION
        # =================================================

        update_status(
            run_id,
            "Final application verified",
            "VERIFY",
            (
                "Resume, evidence, evaluation and "
                "verification checks are complete."
            ),
            "Finalize the application package."
        )

        record_action(
            state,
            "Finalize application",
            "Application package successfully verified."
        )

        time.sleep(1)


        # =================================================
        # STEP 14 — COMPLETED
        # =================================================

        update_state(
            state,
            status="completed"
        )

        runs[run_id]["status"] = "completed"

        runs[run_id]["result"] = {

            "status": "verified",

            "resume_filename":
                f"{run_id}_tailored_resume.pdf",

            "report_filename":
                f"{run_id}_evidence_report.pdf",

            "evaluation":
                evaluation,

            "verification":
                verification,

            "matched_evidence":
                matching["matched"],

            "missing_requirements":
                matching["missing"],

            "replanned":
                replanned,

            "replan_count":
                state["replan_count"],

            "ai_analysis":
                state.get(
                    "ai_analysis",
                    {}
                ),

            "actions":
                state["actions"]
        }


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        runs[run_id]["status"] = "failed"

        runs[run_id]["error"] = str(error)

        update_status(
            run_id,
            "Process failed",
            "ERROR",
            "An unexpected error occurred.",
            "Stop the application workflow."
        )

        record_action(
            state,
            "Workflow error",
            str(error)
        )

        update_state(
            state,
            status="failed"
        )


# ---------------------------------------------------------
# GET CURRENT AGENT STATUS
# ---------------------------------------------------------

def get_status(run_id):

    if run_id not in runs:
        return {
            "status": "not_found"
        }

    run = runs[run_id]

    return {

        "status":
            run.get("status"),

        "current_step":
            run.get("current_step"),

        "decision":
            run.get("decision"),

        "reason":
            run.get("reason"),

        "action":
            run.get("action")
    }


# ---------------------------------------------------------
# GET FINAL RESULT
# ---------------------------------------------------------

def get_result(run_id):

    if run_id not in runs:
        return {
            "status": "not_found"
        }

    run = runs[run_id]

    if "result" not in run:

        return {
            "status":
                run.get("status"),

            "current_step":
                run.get("current_step"),

            "decision":
                run.get("decision"),

            "reason":
                run.get("reason")
        }

    return run["result"]