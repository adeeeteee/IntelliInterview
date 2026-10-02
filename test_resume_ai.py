from resume_parser.parser import extract_text_from_pdf
from ai_engine.resume_extractor import extract_resume_information


file_path = "AdithiBhrugubanda_resume.pdf"

print("Reading resume...")
resume_text = extract_text_from_pdf(file_path)

print("Sending resume to AI...")
result = extract_resume_information(resume_text)

print("\n===== AI EXTRACTED RESUME INFORMATION =====")
print(result)