from ai_engine.performance_report import (
    extract_score,
    calculate_performance_scores
)


class TestAnswer:

    def __init__(
        self,
        evaluation
    ):
        self.evaluation = evaluation


# Sample AI evaluations
answers = [

    TestAnswer("""
Relevance: 8/10
Content Accuracy: 9/10
Completeness: 7/10
Clarity: 9/10
Overall Score: 8.2/10
"""),

    TestAnswer("""
Relevance: 6/10
Content Accuracy: 8/10
Completeness: 8/10
Clarity: 7/10
Overall Score: 7.3/10
"""),

    TestAnswer("""
Relevance: 9/10
Content Accuracy: 9/10
Completeness: 8/10
Clarity: 8/10
Overall Score: 8.5/10
""")

]


# Test individual score extraction

print("\n===== SCORE EXTRACTION TEST =====")

evaluation = answers[0].evaluation

print(
    "Relevance:",
    extract_score(
        evaluation,
        "Relevance"
    )
)

print(
    "Content Accuracy:",
    extract_score(
        evaluation,
        "Content Accuracy"
    )
)

print(
    "Completeness:",
    extract_score(
        evaluation,
        "Completeness"
    )
)

print(
    "Clarity:",
    extract_score(
        evaluation,
        "Clarity"
    )
)

print(
    "Overall Score:",
    extract_score(
        evaluation,
        "Overall Score"
    )
)


# Test average calculation

scores = calculate_performance_scores(
    answers
)

print("\n===== PERFORMANCE SCORE TEST =====")

print(
    "Relevance:",
    scores["relevance"]
)

print(
    "Content Accuracy:",
    scores["content_accuracy"]
)

print(
    "Completeness:",
    scores["completeness"]
)

print(
    "Clarity:",
    scores["clarity"]
)

print(
    "Overall:",
    scores["overall"]
)