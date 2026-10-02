import re


SECTION_HEADINGS = [
    "CAREER OBJECTIVE",
    "EDUCATION",
    "VIRTUAL EXPERIENCE",
    "TECHNICAL SKILLS",
    "PROJECTS",
    "CERTIFICATIONS",
    "ACHIEVEMENTS & ACTIVITIES",
    "STRENGTHS"
]


def split_resume_sections(resume_text):
    sections = {}

    pattern = "|".join(
        re.escape(heading) for heading in SECTION_HEADINGS
    )

    matches = list(
        re.finditer(
            rf"^\s*({pattern})\s*$",
            resume_text,
            flags=re.IGNORECASE | re.MULTILINE
        )
    )

    for index, match in enumerate(matches):
        heading = match.group(1).upper().strip()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(resume_text)

        section_text = resume_text[start:end].strip()

        sections[heading] = section_text

    return sections