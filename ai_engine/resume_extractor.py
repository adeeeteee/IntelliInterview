from ai_engine.client import ask_ai
from models.resume import ResumeData, Project

import re


def clean_response(response):
    return response.strip()


def extract_section(section_text, section_name, instructions):

    prompt = f"""
You are a resume information extraction assistant.

Extract information ONLY from the {section_name} section provided below.

{instructions}

Do not use information from any other resume section.
Do not invent information.
Do not add explanations or commentary.

Section content:

{section_text}
"""

    response = ask_ai(prompt)

    return clean_response(response)


def extract_basic_information(resume_text):

    prompt = f"""
You are a resume information extraction assistant.

Extract only:
- Full name
- Email address

Do not invent information.

Return exactly in this format:

Name: ...
Email: ...

Resume:

{resume_text}
"""

    return clean_response(ask_ai(prompt))


def extract_education(section_text):

    instructions = """
Extract each education entry.

For each entry include:
- Institution
- Degree or qualification
- Field of study
- Dates
- CGPA if available

Return each entry as a separate numbered item.
"""

    return extract_section(
        section_text,
        "education",
        instructions
    )


def extract_skills(section_text):

    instructions = """
Extract all technical skills.

Include:
- Programming languages
- Frameworks
- Databases
- Web technologies
- Machine learning/data tools
- DevOps/cloud tools
- Blockchain tools
- Development tools

Return only a comma-separated list.
"""

    return extract_section(
        section_text,
        "technical skills",
        instructions
    )


def extract_projects(section_text):

    instructions = """
Extract EVERY project present in the projects section.

For each project provide:

PROJECT: Project name
TECHNOLOGIES: technology1, technology2, technology3
DESCRIPTION: Short project description

IMPORTANT:

- Do not skip any project.
- Do not merge different projects.
- Do not invent technologies.
- Do not infer technologies from the general skills section.
- Only include technologies explicitly associated with that project
  in the provided project section.
- Keep each project's technologies separate.
- If no technologies are explicitly mentioned, write:
  TECHNOLOGIES: None
- Do not include certifications, education, achievements, or strengths.

Return ONLY the projects in this format.

Example:

PROJECT: Example Project
TECHNOLOGIES: Python, Flask, SQLite
DESCRIPTION: Short description of the project.

PROJECT: Another Project
TECHNOLOGIES: Java, Spring Boot
DESCRIPTION: Short description of the project.

Do not use JSON.
Do not add explanations.
"""

    return extract_section(
        section_text,
        "projects",
        instructions
    )


def extract_experience(section_text):

    instructions = """
Extract each professional or virtual experience.

For each experience include:
- Organization/company
- Role or program name
- Main work performed
- Technologies/tools used

Return each experience as a separate numbered item.
"""

    return extract_section(
        section_text,
        "virtual experience",
        instructions
    )


def extract_certifications(section_text):

    instructions = """
Extract EVERY certification or certification course from this section.

IMPORTANT:

- Each complete certification must be ONE numbered item.
- Keep the provider name and certification name together.
- Do not split provider names from certification names.
- Do not merge different certifications.
- Do not invent certifications.
- Extract every certification present.

For example:

1. Infosys Springboard: Introduction to Python
2. Infosys Springboard: Programming in C
3. Infosys Springboard: Project Management with Agile
4. Infosys Springboard: Generative AI for Professionals
5. Scaler: Fundamentals of Docker and Kubernetes
6. NPTEL: Human-Computer Interaction

Return only the certifications as numbered items.
"""

    return extract_section(
        section_text,
        "certifications",
        instructions
    )


def parse_basic_information(text):

    name_match = re.search(
        r"Name:\s*(.+)",
        text
    )

    email_match = re.search(
        r"Email:\s*([^\s|]+)",
        text
    )

    name = (
        name_match.group(1).strip()
        if name_match
        else ""
    )

    email = (
        email_match.group(1).strip()
        if email_match
        else ""
    )

    return name, email


def parse_numbered_items(text):

    items = []

    matches = re.split(
        r"\n(?=\d+\.)",
        text.strip()
    )

    for item in matches:

        item = item.strip()

        if item:

            item = re.sub(
                r"^\d+\.\s*",
                "",
                item
            )

            items.append(item)

    return items


def parse_projects(text):

    projects = []

    # Separate each project using PROJECT: as the starting point
    blocks = re.split(
        r"\n\s*(?=PROJECT:)",
        text.strip()
    )

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        name_match = re.search(
            r"PROJECT:\s*(.+)",
            block
        )

        technologies_match = re.search(
            r"TECHNOLOGIES:\s*(.+)",
            block
        )

        description_match = re.search(
            r"DESCRIPTION:\s*(.+)",
            block,
            re.DOTALL
        )

        name = (
            name_match.group(1).strip()
            if name_match
            else ""
        )

        technologies = []

        if technologies_match:

            technology_text = (
                technologies_match.group(1).strip()
            )

            if technology_text.lower() != "none":

                technologies = [
                    technology.strip()
                    for technology in technology_text.split(",")
                    if technology.strip()
                ]

        description = (
            description_match.group(1).strip()
            if description_match
            else ""
        )

        if name:

            projects.append(
                Project(
                    name=name,
                    technologies=technologies,
                    description=description
                )
            )

    return projects


def extract_resume_data(resume_text, sections):

    basic_information = extract_basic_information(
        resume_text
    )

    education = extract_education(
        sections.get("EDUCATION", "")
    )

    skills = extract_skills(
        sections.get("TECHNICAL SKILLS", "")
    )

    projects = extract_projects(
        sections.get("PROJECTS", "")
    )

    experience = extract_experience(
        sections.get("VIRTUAL EXPERIENCE", "")
    )

    certifications = extract_certifications(
        sections.get("CERTIFICATIONS", "")
    )

    name, email = parse_basic_information(
        basic_information
    )

    resume_data = ResumeData(
        name=name,
        email=email,

        education=parse_numbered_items(
            education
        ),

        skills=[
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ],

        projects=parse_projects(
            projects
        ),

        experience=parse_numbered_items(
            experience
        ),

        certifications=parse_numbered_items(
            certifications
        )
    )

    return resume_data