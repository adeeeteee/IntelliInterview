from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract ONLY the candidate's work experience or professional
virtual experience.

For each experience, provide:
- Organization/company
- Role or program name
- Main responsibilities or work performed
- Technologies/tools used if mentioned

Do NOT include:
- Education
- Projects
- Certifications
- Skills
- Achievements

Return each experience as a separate numbered item.

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== AI EXPERIENCE EXTRACTION =====")
print(result)