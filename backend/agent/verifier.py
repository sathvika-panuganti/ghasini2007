import re


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return set(text.split())


def verify_application(
    original_resume,
    generated_resume,
    matched_evidence
):

    if not generated_resume:
        return {
            "passed": False,
            "message": "Generated resume is empty.",
            "unsupported_claims": []
        }

    original_words = normalize(original_resume)
    generated_words = normalize(generated_resume)

    unsupported = []

    for evidence in matched_evidence:

        evidence_words = normalize(evidence)

        if not evidence_words.issubset(generated_words):
            unsupported.append(evidence)

    suspicious_count = 0

    for word in generated_words:
        if len(word) > 5 and word not in original_words:
            suspicious_count += 1

    passed = len(unsupported) == 0

    return {
        "passed": passed,
        "message": (
            "Final application passed verification."
            if passed
            else "Verification found unsupported evidence."
        ),
        "unsupported_claims": unsupported,
        "new_word_count": suspicious_count
    }