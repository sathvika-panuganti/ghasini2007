from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_resume(
    resume_text,
    target_role,
    matched_skills,
    output_path
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


    title_style = styles["Title"]

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]


    story = []


    # ==========================================
    # TITLE
    # ==========================================

    story.append(
        Paragraph(
            "TAILORED RESUME",
            title_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    story.append(
        Paragraph(
            f"Target Role: {target_role}",
            heading_style
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # RELEVANT SKILLS
    # ==========================================

    story.append(
        Paragraph(
            "Relevant Skills",
            heading_style
        )
    )


    if matched_skills:

        skills_text = ", ".join(
            matched_skills
        )

    else:

        skills_text = "No directly matched skills found."


    story.append(
        Paragraph(
            skills_text,
            body_style
        )
    )


    story.append(
        Spacer(1, 15)
    )


    # ==========================================
    # ORIGINAL INFORMATION
    # ==========================================

    story.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )


    for line in resume_text.splitlines():

        if line.strip():

            safe_line = (
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_line,
                    body_style
                )
            )

            story.append(
                Spacer(1, 4)
            )


    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            "Guardrail: Only information found in "
            "the original candidate resume was used.",
            body_style
        )
    )


    document.build(story)


    return output_path