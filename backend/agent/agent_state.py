from datetime import datetime


def create_initial_state(run_id, target_role, job_url):
    return {
        "run_id": run_id,
        "goal": f"Create the best truthful resume for the role: {target_role}",

        "target_role": target_role,
        "job_url": job_url,

        "status": "starting",

        "resume_text": "",
        "candidate_evidence": {},

        "job_text": "",
        "job_requirements": [],

        "matched_evidence": [],
        "missing_requirements": [],

        "ai_analysis": {},
        "plan": [],

        "actions": [],
        "observations": [],

        "evaluation": {},

        "replan_count": 0,
        "max_replans": 2,

        "verification": {},

        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def record_action(state, action, observation):
    state["actions"].append({
        "action": action,
        "observation": observation,
        "time": datetime.now().isoformat()
    })

    state["observations"].append(observation)
    state["updated_at"] = datetime.now().isoformat()


def update_state(state, **kwargs):
    for key, value in kwargs.items():
        state[key] = value

    state["updated_at"] = datetime.now().isoformat()