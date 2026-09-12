import re


COMMON_REQUIREMENTS = [

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


def extract_job_requirements(job_text):

    text = job_text.lower()

    requirements = []


    for requirement in COMMON_REQUIREMENTS:

        if re.search(
            r"\b" + re.escape(requirement) + r"\b",
            text
        ):

            requirements.append(requirement)


    return requirements


def match_evidence(
    candidate_evidence,
    job_requirements
):

    candidate_skills = set(
        candidate_evidence["skills"]
    )


    matched = []

    missing = []


    for requirement in job_requirements:

        if requirement in candidate_skills:

            matched.append(requirement)

        else:

            missing.append(requirement)


    return {

        "matched": matched,

        "missing": missing,

        "total_requirements":
            len(job_requirements)

    }