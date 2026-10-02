import re

from ai_engine.client import ask_ai


def extract_score(
    evaluation,
    criterion
):

    pattern = rf"{re.escape(criterion)}:\s*(\d+(?:\.\d+)?)\/10"

    match = re.search(
        pattern,
        evaluation,
        re.IGNORECASE
    )

    if match:

        return float(
            match.group(1)
        )

    return None


def calculate_performance_scores(
    answers
):

    relevance_scores = []
    accuracy_scores = []
    completeness_scores = []
    clarity_scores = []
    overall_scores = []

    for answer in answers:

        evaluation = answer.evaluation

        relevance = extract_score(
            evaluation,
            "Relevance"
        )

        accuracy = extract_score(
            evaluation,
            "Content Accuracy"
        )

        completeness = extract_score(
            evaluation,
            "Completeness"
        )

        clarity = extract_score(
            evaluation,
            "Clarity"
        )

        overall = extract_score(
            evaluation,
            "Overall Score"
        )

        if relevance is not None:
            relevance_scores.append(
                relevance
            )

        if accuracy is not None:
            accuracy_scores.append(
                accuracy
            )

        if completeness is not None:
            completeness_scores.append(
                completeness
            )

        if clarity is not None:
            clarity_scores.append(
                clarity
            )

        if overall is not None:
            overall_scores.append(
                overall
            )

    def calculate_average(scores):

        if not scores:
            return 0.0

        return round(
            sum(scores) / len(scores),
            2
        )

    return {
        "relevance": calculate_average(
            relevance_scores
        ),
        "content_accuracy": calculate_average(
            accuracy_scores
        ),
        "completeness": calculate_average(
            completeness_scores
        ),
        "clarity": calculate_average(
            clarity_scores
        ),
        "overall": calculate_average(
            overall_scores
        )
    }


def generate_performance_report(
    interview_context,
    personalized_feedback,
    performance_scores
):

    prompt = f"""
You are an AI interview performance analyst.

Analyze the candidate's complete interview history,
personalized feedback, and calculated performance scores.

INTERVIEW HISTORY:
{interview_context}

PERSONALIZED FEEDBACK:
{personalized_feedback}

CALCULATED PERFORMANCE SCORES:
Relevance: {performance_scores["relevance"]}/10
Content Accuracy: {performance_scores["content_accuracy"]}/10
Completeness: {performance_scores["completeness"]}/10
Clarity: {performance_scores["clarity"]}/10
Overall Score: {performance_scores["overall"]}/10

Generate a final interview performance report.

The report should include:

1. Overall Score
2. Category Scores
3. Key Strengths
4. Areas for Improvement
5. Recommendations

IMPORTANT:

- Use the calculated scores exactly as provided.
- Do NOT recalculate or change the scores.
- Base qualitative observations only on the interview
  history and personalized feedback.
- Do not invent candidate information.
- Do not assume skills that were not demonstrated.
- Keep the report concise and practical.

Return ONLY in this format:

Overall Score: {performance_scores["overall"]}/10

Category Scores:
Relevance: {performance_scores["relevance"]}/10
Content Accuracy: {performance_scores["content_accuracy"]}/10
Completeness: {performance_scores["completeness"]}/10
Clarity: {performance_scores["clarity"]}/10

Key Strengths:
- ...

Areas for Improvement:
- ...

Recommendations:
- ...
"""

    response = ask_ai(prompt)

    return response.strip()