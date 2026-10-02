from resume_parser.parser import extract_text_from_pdf
from resume_parser.section_splitter import split_resume_sections
from ai_engine.resume_extractor import extract_resume_data


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

sections = split_resume_sections(resume_text)

resume_data = extract_resume_data(
    resume_text,
    sections
)

print("\n===== AI EXTRACTED RESUME DATA =====")

for section, content in resume_data.items():
    print(f"\n--- {section.upper()} ---")
    print(content)