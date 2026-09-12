from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    output_path,
    target_role,
    matched,
    missing,
    evaluation,
    verification
):

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    styles = getSampleStyleSheet()


    story = []


    story.append(
        Paragraph(
            "Evidence & Change Report",
            styles["Title"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            f"Target Role: {target_role}",
            styles["Heading2"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # MATCHED
    # ==========================================

    story.append(
        Paragraph(
            "Evidence Used",
            styles["Heading2"]
        )
    )


    if matched:

        text = ", ".join(matched)

    else:

        text = "No directly matched requirements."


    story.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # MISSING
    # ==========================================

    story.append(
        Paragraph(
            "Requirements Without Evidence",
            styles["Heading2"]
        )
    )


    if missing:

        text = ", ".join(missing)

    else:

        text = "None"


    story.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # EVALUATION
    # ==========================================

    story.append(
        Paragraph(
            "Evaluation",
            styles["Heading2"]
        )
    )


    evaluation_text = f"""
    ATS Score: {evaluation["ats_score"]}%<br/>
    Job Relevance: {evaluation["relevance_score"]}%<br/>
    Evidence Coverage: {evaluation["evidence_score"]}%<br/>
    Factual Consistency: {evaluation["factual_consistency"]}<br/>
    Formatting: {evaluation["formatting"]}
    """


    story.append(
        Paragraph(
            evaluation_text,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # VERIFICATION
    # ==========================================

    story.append(
        Paragraph(
            "Verification",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            verification["message"],
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            "Guardrail: The system must never "
            "invent skills, projects, certificates, "
            "employment or achievements.",
            styles["BodyText"]
        )
    )


    document.build(story)


    return output_path