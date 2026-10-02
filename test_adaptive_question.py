from ai_engine.adaptive_question import generate_adaptive_question


previous_question = (
    "What is Python, and what are its common uses in software development?"
)

candidate_answer = """
Python is a high-level programming language.
It is commonly used for web development,
automation, and data analysis.
"""

evaluation = """
Relevance: 8/10
Content Accuracy: 9/10
Completeness: 6/10
Clarity: 9/10
Overall Score: 8/10
Feedback: The answer is accurate and clear but could
explain more about Python's applications.
"""


result = generate_adaptive_question(
    previous_question,
    candidate_answer,
    evaluation
)


print("\n===== ADAPTIVE QUESTION =====")
print(result)