from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract the candidate's education information.

For each education entry, include:
- Institution name
- Degree or qualification
- Field of study if available
- Dates if available

Return each education entry as a separate numbered item.
Do not explain anything else.

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== AI EDUCATION EXTRACTION =====")
print(result)