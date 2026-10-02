from resume_parser.parser import extract_text_from_pdf
from resume_parser.section_splitter import split_resume_sections


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

sections = split_resume_sections(resume_text)


print("===== RESUME SECTIONS =====")

for section_name, content in sections.items():
    print(f"\n--- {section_name} ---")
    print(content[:500])