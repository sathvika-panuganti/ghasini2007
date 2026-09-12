import re


SKILLS = [

    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "c",
    "c++",
    "react",
    "node.js",
    "node",
    "django",
    "flask",
    "fastapi",
    "mongodb",
    "mysql",
    "postgresql",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "api",
    "rest api",
    "aws",
    "docker",
    "linux",
    "communication",
    "leadership",
    "teamwork"
]


def extract_evidence(resume_text):

    text = resume_text.lower()


    found_skills = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text
        ):

            found_skills.append(skill)


    # ==========================================
    # Sections
    # ==========================================

    sections = {

        "skills": [],

        "projects": [],

        "education": [],

        "experience": [],

        "achievements": []

    }


    lines = resume_text.splitlines()


    current_section = None


    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue


        lower_line = clean_line.lower()


        if "skill" in lower_line:

            current_section = "skills"

        elif "project" in lower_line:

            current_section = "projects"

        elif "education" in lower_line:

            current_section = "education"

        elif (
            "experience" in lower_line
            or "internship" in lower_line
        ):

            current_section = "experience"

        elif (
            "achievement" in lower_line
            or "award" in lower_line
        ):

            current_section = "achievements"


        elif current_section:

            sections[current_section].append(
                clean_line
            )


    return {

        "skills": found_skills,

        "sections": sections,

        "raw_text": resume_text

    }