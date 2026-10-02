from resume_parser.parser import extract_text_from_pdf
from ai_engine.resume_extractor import extract_resume_data


file_path = "AdithiBhrugubanda_resume.pdf"

print("Reading resume...")
resume_text = extract_text_from_pdf(file_path)

print("Extracting resume information using AI...")
resume_data = extract_resume_data(resume_text)

print("\n===== COMPLETE AI EXTRACTION =====")

for section, content in resume_data.items():
    print(f"\n--- {section.upper()} ---")
    print(content)