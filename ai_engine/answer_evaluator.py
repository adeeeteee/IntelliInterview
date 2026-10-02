from ai_engine.client import ask_ai


def evaluate_answer(question, answer):

    prompt = f"""
You are an AI interview answer evaluator.

Evaluate the candidate's answer to the interview question below.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer using these four criteria:

1. Relevance
2. Content Accuracy
3. Completeness
4. Clarity

Give a score from 1 to 10 for each criterion.

Also provide:
- Overall score from 1 to 10
- One short feedback statement

STRICT RULES:

- Evaluate only the candidate's answer.
- Do not invent information about the candidate.
- Do not assume knowledge that is not present in the answer.
- Keep feedback concise.
- Return ONLY in the following format:

Relevance: X/10
Content Accuracy: X/10
Completeness: X/10
Clarity: X/10
Overall Score: X/10
Feedback: ...
"""

    response = ask_ai(prompt)

    return response.strip()