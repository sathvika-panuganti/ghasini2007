import os
import json
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def ask_agent(
    resume_text,
    job_text,
    target_role,
    candidate_evidence,
    job_requirements,
    evaluation=None
):

    prompt = f"""
You are an autonomous resume application agent.

GOAL:
Create the strongest possible resume for the target job
WITHOUT FABRICATING ANY INFORMATION.

TARGET ROLE:
{target_role}

CANDIDATE RESUME:
{resume_text}

CANDIDATE EVIDENCE:
{json.dumps(candidate_evidence)}

JOB POSTING:
{job_text}

JOB REQUIREMENTS:
{json.dumps(job_requirements)}

CURRENT EVALUATION:
{json.dumps(evaluation or {})}

STRICT RULES:

1. Never invent skills.
2. Never invent projects.
3. Never invent employment.
4. Never invent internships.
5. Never invent certificates.
6. Never invent achievements.
7. Never invent education.
8. Never claim a requirement unless supported by resume evidence.
9. Prefer existing evidence over assumptions.
10. If the previous attempt failed, create a different plan.

Decide what the agent should do next.

Return ONLY JSON:

{{
    "decision": "TAILOR | REPLAN | REJECT | VERIFY",
    "reason": "short explanation",

    "plan": [
        "specific action 1",
        "specific action 2"
    ],

    "supported_evidence": [
        "evidence from resume"
    ],

    "unsupported_requirements": [
        "job requirements without evidence"
    ],

    "risk_warnings": [
        "things the system must not claim"
    ]
}}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    text = response.output_text

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "decision": "VERIFY",
            "reason": "AI response could not be parsed.",
            "plan": [],
            "supported_evidence": [],
            "unsupported_requirements": [],
            "risk_warnings": [
                "Invalid AI response."
            ]
        }