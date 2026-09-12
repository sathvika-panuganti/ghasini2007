def evaluate_application(
    matched,
    missing,
    required_keywords=None
):
    """
    Evaluate how well the candidate's genuine evidence
    matches the job requirements.

    This evaluator does NOT invent or assume skills.
    It only evaluates evidence that was already extracted
    from the candidate's resume.
    """

    # Make sure we have lists
    matched = matched or []
    missing = missing or []

    # Total number of requirements considered
    total_requirements = len(matched) + len(missing)

    # Calculate evidence coverage
    if total_requirements == 0:
        evidence_score = 0
    else:
        evidence_score = round(
            (len(matched) / total_requirements) * 100
        )

    # -------------------------------------------------
    # ATS SCORE
    # -------------------------------------------------
    # Prototype ATS score based on supported requirements.
    ats_score = evidence_score

    # -------------------------------------------------
    # JOB RELEVANCE SCORE
    # -------------------------------------------------
    relevance_score = evidence_score

    # -------------------------------------------------
    # DECISION
    # -------------------------------------------------
    # The agent should replan when the evidence coverage
    # is below the target.
    if evidence_score >= 80:
        decision = "PASS"

    elif evidence_score >= 60:
        decision = "REPLAN"

    else:
        decision = "REPLAN"

    # -------------------------------------------------
    # REASON
    # -------------------------------------------------
    if evidence_score >= 80:
        reason = (
            "Most job requirements are supported by "
            "evidence from the candidate resume."
        )

    elif evidence_score >= 60:
        reason = (
            "Some important job requirements are not "
            "supported by candidate evidence. "
            "The agent should replan without inventing information."
        )

    else:
        reason = (
            "Evidence coverage is low. "
            "The agent should replan and emphasize only "
            "genuine candidate evidence."
        )

    # -------------------------------------------------
    # RETURN EVALUATION
    # -------------------------------------------------
    return {
        "ats_score": ats_score,

        "relevance_score": relevance_score,

        "evidence_score": evidence_score,

        "factual_consistency": "PENDING",

        "decision": decision,

        "reason": reason,

        "matched_count": len(matched),

        "missing_count": len(missing),

        "matched_requirements": matched,

        "missing_requirements": missing,

        "total_requirements": total_requirements
    }