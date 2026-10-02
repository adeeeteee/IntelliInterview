from ai_engine.feedback_generator import (
    build_interview_context,
    generate_personalized_feedback
)


# Sample interview history
interview_answers = [

    {
        "question_number": 1,
        "question": "What is Python, and what are its common uses in software development?",
        "answer": "Python is a high-level programming language used for web development, automation, data analysis and scripting.",
        "evaluation": """
Relevance: 8/10
Content Accuracy: 9/10
Completeness: 7/10
Clarity: 9/10
Overall Score: 8.2/10
"""
    },

    {
        "question_number": 2,
        "question": "What is NumPy and why is it useful?",
        "answer": "NumPy is a Python library used for numerical computing. It provides arrays and mathematical operations.",
        "evaluation": """
Relevance: 9/10
Content Accuracy: 9/10
Completeness: 8/10
Clarity: 8/10
Overall Score: 8.5/10
"""
    }

]


# Convert the sample history into interview context
interview_context = ""

for answer in interview_answers:

    interview_context += f"""
Question {answer["question_number"]}:
{answer["question"]}

Candidate Answer:
{answer["answer"]}

AI Evaluation:
{answer["evaluation"]}

-------------------------
"""


# Generate personalized feedback
feedback = generate_personalized_feedback(
    interview_context
)


print("\n===== PERSONALIZED FEEDBACK =====")
print(feedback)