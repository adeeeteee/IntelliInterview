from ai_engine.client import ask_ai


def build_interview_context(answers):

    interview_context = ""

    for answer in answers:

        interview_context += f"""
Question {answer.question_number}:
{answer.question}

Candidate Answer:
{answer.answer}

AI Evaluation:
{answer.evaluation}

-------------------------
"""

    return interview_context.strip()


def generate_personalized_feedback(
    interview_context
):

    prompt = f"""
You are an AI interview feedback assistant.

Analyze the candidate's interview history below.

Interview History:
{interview_context}

Based only on the interview history, provide personalized
feedback about the candidate's performance.

Focus on:

1. Strengths
2. Areas for Improvement
3. Specific Recommendations

STRICT RULES:

- Base the feedback only on the interview history.
- Do not invent information about the candidate.
- Do not make assumptions about skills that were not demonstrated.
- Identify patterns across multiple answers when possible.
- Keep the feedback concise and practical.
- Provide specific observations rather than generic advice.

Return the result in exactly this format:

Strengths:
- ...

Areas for Improvement:
- ...

Recommendations:
- ...
"""

    response = ask_ai(prompt)

    return response.strip()