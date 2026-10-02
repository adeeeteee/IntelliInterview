from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract ONLY the candidate's certifications.

For each certification, provide:
- Certification/provider
- Certification or course name

Do NOT include:
- Education
- Projects
- Work experience
- Virtual experience
- Skills
- Achievements

Return each certification as a separate numbered item.

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== AI CERTIFICATION EXTRACTION =====")
print(result)