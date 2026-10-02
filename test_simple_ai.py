from resume_parser.parser import extract_text_from_pdf
from ai_engine.client import ask_ai


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

prompt = f"""
Read the resume below.

Extract only:
1. The person's full name
2. Their email address

Return exactly two lines:

Name: ...
Email: ...

Resume:
{resume_text}
"""

result = ask_ai(prompt)

print("===== SIMPLE AI EXTRACTION =====")
print(result)