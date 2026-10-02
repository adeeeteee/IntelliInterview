from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract ONLY the candidate's PROJECTS.

For each project, provide:
- Project title
- Technologies/tools used
- A short description of what was done

IMPORTANT:
Do NOT include education, certifications, virtual experiences,
work experience, achievements, or strengths.

Return each project as a separate numbered item.

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== AI PROJECT EXTRACTION =====")
print(result)