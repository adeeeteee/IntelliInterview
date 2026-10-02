from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract the candidate's technical skills.

Include:
- Programming languages
- Frameworks
- Databases
- Tools
- Cloud/DevOps technologies
- Blockchain technologies
- Data/ML technologies

Return only a simple comma-separated list.
Do not explain anything.

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== AI SKILLS EXTRACTION =====")
print(result)