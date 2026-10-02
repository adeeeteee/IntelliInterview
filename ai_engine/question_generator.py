from ai_engine.client import ask_ai


# Common technologies that the AI might incorrectly introduce.
# We use this list to detect technologies that are not present
# in the candidate's resume.
COMMON_TECHNOLOGIES = {
    "node.js",
    "nodejs",
    "express",
    "express.js",
    "django",
    "flask",
    "fastapi",
    "cassandra",
    "postgresql",
    "postgres",
    "mysql",
    "redis",
    "firebase",
    "aws",
    "aws lambda",
    "amazon s3",
    "s3",
    "azure",
    "google cloud",
    "gcp",
    "kubernetes",
    "docker",
    "react",
    "react.js",
    "angular",
    "vue",
    "tensorflow",
    "pytorch",
    "keras",
    "scipy",
    "spark",
    "apache spark",
    "kafka",
    "jenkins",
    "gitlab",
    "github actions",
    "oracle",
    "sqlite",
    "mariadb",
    "php",
    "ruby",
    "rails",
    "c++",
    "c#",
    "go",
    "golang",
    "rust",
    "swift",
    "kotlin",
    "typescript",
    "next.js",
    "spring",
    "spring boot",
    "mongodb",
    "sql",
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "solidity",
    "ethereum",
    "ganache",
    "metamask",
    "remix ide",
    "wazuh",
    "telegram bot api",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
}


def normalize_text(text):
    return text.lower().strip()


def clean_question(question):

    question = question.strip()

    prefixes = [
        "here is a technical interview question:",
        "here's a technical interview question:",
        "here is a technical interview question that meets your requirements:",
        "here's a technical interview question that meets your requirements:",
        "here is a potential technical interview question:",
        "here's a potential technical interview question:",
        "technical interview question:",
        "interview question:",
        "here is a potential interview question:",
        "here's a potential interview question:",
        "here is a single interview question:",
        "here's a single interview question:"
    ]

    question_lower = question.lower()

    for prefix in prefixes:

        if question_lower.startswith(prefix):

            question = question[
                len(prefix):
            ].strip()

            break

    return question


def get_allowed_technologies(resume_data):

    allowed = set()

    # Technologies from the general skills section
    for skill in resume_data.skills:
        allowed.add(
            normalize_text(skill)
        )

    # Technologies from individual projects
    for project in resume_data.projects:
        for technology in project.technologies:
            allowed.add(
                normalize_text(technology)
            )

    return allowed


def find_unapproved_technologies(
    question,
    allowed_technologies
):

    question_lower = normalize_text(
        question
    )

    unapproved = []

    for technology in COMMON_TECHNOLOGIES:

        if technology in question_lower:

            if technology not in allowed_technologies:

                unapproved.append(
                    technology
                )

    return unapproved


def is_valid_question(
    question,
    allowed_technologies
):

    if not question:
        return False

    unapproved = find_unapproved_technologies(
        question,
        allowed_technologies
    )

    return len(unapproved) == 0


def extract_numbered_questions(text):

    questions = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():

            parts = line.split(".", 1)

            if len(parts) == 2:

                question = parts[1].strip()

                if question:

                    questions.append(
                        clean_question(question)
                    )

    return questions


def generate_technical_question(
    resume_data
):

    skills = ", ".join(
        resume_data.skills
    )

    allowed_technologies = (
        get_allowed_technologies(
            resume_data
        )
    )

    prompt = f"""
Generate ONE technical interview question.

Candidate technical skills:

{skills}

STRICT RULES:

- Ask exactly ONE question.
- Use ONLY the technologies listed above.
- Do NOT mention any other technology.
- Do NOT compare a listed technology with an unlisted technology.
- Do not invent project usage.
- Test technical understanding.
- Return ONLY the question.
- Do not write introductions.
- Do not write explanations.
- Do not write phrases such as "Here is a question".
"""

    for attempt in range(3):

        response = ask_ai(prompt)

        question = clean_question(
            response
        )

        if is_valid_question(
            question,
            allowed_technologies
        ):

            return question

    # Safe fallback
    if resume_data.skills:

        skill = resume_data.skills[0]

        return (
            f"What is {skill}, and what are its common uses "
            f"in software development?"
        )

    return (
        "What technical skill are you most comfortable "
        "working with?"
    )


def generate_project_question(
    project,
    resume_data
):

    technologies = ", ".join(
        project.technologies
    )

    allowed_technologies = (
        get_allowed_technologies(
            resume_data
        )
    )

    prompt = f"""
Generate ONE interview question about this candidate project.

Project:
{project.name}

Technologies explicitly associated with this project:
{technologies}

Description:
{project.description}

STRICT RULES:

- Ask exactly ONE question.
- The question must be about this project.
- You may mention ONLY technologies listed above.
- Do NOT introduce any other technology.
- Do NOT invent project functionality.
- Do not ask the candidate to simply list technologies.
- Ask about purpose, implementation, design, challenges,
  or use of an explicitly listed technology.
- Return ONLY the question.
- Do not write introductions.
- Do not write explanations.
- Do not write phrases such as "Here is a question".
"""

    for attempt in range(3):

        response = ask_ai(prompt)

        question = clean_question(
            response
        )

        if (
            is_valid_question(
                question,
                allowed_technologies
            )
            and project.name.lower()
            in question.lower()
        ):

            return question

    # Safe fallback
    return (
        f"What was the main purpose of your "
        f"{project.name}, and what did you learn "
        f"while developing it?"
    )


def generate_hr_questions():

    prompt = """
Generate exactly TWO HR interview questions for an
entry-level software engineering candidate.

Focus on:

- Communication
- Teamwork
- Motivation
- Adaptability
- Learning attitude
- Problem-solving
- Career goals

STRICT RULES:

- These must be HR questions.
- Do NOT ask technical questions.
- Do NOT mention programming languages.
- Do NOT mention frameworks.
- Do NOT mention databases.
- Do NOT mention tools.
- Do NOT mention algorithms.
- Do NOT mention technical implementation.
- Return ONLY the two questions.
"""

    response = ask_ai(prompt)

    questions = extract_numbered_questions(
        response
    )

    if len(questions) >= 2:

        return questions[:2]

    # Safe fallback questions
    return [
        "How do you approach learning something new when you do not have prior experience with it?",
        "Tell me about a time when you had to work with others to complete a task."
    ]


def generate_questions(resume_data):

    # --------------------------------
    # TECHNICAL QUESTIONS
    # --------------------------------

    technical_questions = []

    for _ in range(3):

        question = generate_technical_question(
            resume_data
        )

        technical_questions.append(
            question
        )

    # --------------------------------
    # PROJECT QUESTIONS
    # --------------------------------

    project_questions = []

    for project in resume_data.projects[:3]:

        question = generate_project_question(
            project,
            resume_data
        )

        project_questions.append(
            question
        )

    # --------------------------------
    # HR QUESTIONS
    # --------------------------------

    hr_questions = generate_hr_questions()

    # --------------------------------
    # FINAL OUTPUT
    # --------------------------------

    result = "TECHNICAL:\n"

    for index, question in enumerate(
        technical_questions,
        start=1
    ):

        result += (
            f"{index}. {question}\n"
        )

    result += "\nPROJECT:\n"

    for index, question in enumerate(
        project_questions,
        start=1
    ):

        result += (
            f"{index}. {question}\n"
        )

    result += "\nHR:\n"

    for index, question in enumerate(
        hr_questions,
        start=1
    ):

        result += (
            f"{index}. {question}\n"
        )

    return result.strip()