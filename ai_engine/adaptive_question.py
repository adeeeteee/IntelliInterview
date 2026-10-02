from ai_engine.client import ask_ai


def generate_adaptive_question(
    previous_question,
    candidate_answer,
    evaluation,
    interview_context=""
):

    prompt = f"""
You are an AI interviewer conducting an adaptive interview.

Previous Interview Question:
{previous_question}

Candidate Answer:
{candidate_answer}

AI Evaluation:
{evaluation}

Previous Interview Context:
{interview_context}

Based on the candidate's answer, evaluation, and previous
interview context, generate ONE appropriate follow-up
interview question.

ADAPTIVE RULES:

- If the answer is strong and demonstrates good understanding,
  ask a more advanced or deeper follow-up question.

- If the answer is weak or shows limited understanding,
  ask a simpler question that checks the basic concept.

- If the answer is incomplete,
  ask a follow-up question targeting the missing information.

- The next question must be related to the previous discussion.

- Use the previous interview context to understand what
  topics have already been discussed.

- Do not repeatedly ask the same question.

- Do not suddenly change to an unrelated topic.

- Do not introduce technologies that were not mentioned
  in the interview context, previous question, or candidate answer.

- Do not ask the candidate to simply repeat their previous answer.

- Ask exactly ONE question.

- Return ONLY the question.

- Do not write introductions.
- Do not write explanations.
- Do not write "Here is your next question".
"""

    response = ask_ai(prompt)

    return response.strip()