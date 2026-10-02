from ai_engine.answer_evaluator import evaluate_answer


question = "What is Python, and what are its common uses in software development?"

answer = """
Python is a high-level, interpreted programming language.
It is commonly used for web development, automation,
data analysis, artificial intelligence, and machine learning.
"""


result = evaluate_answer(
    question,
    answer
)


print("\n===== AI ANSWER EVALUATION =====")
print(result)