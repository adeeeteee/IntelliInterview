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

print("\n===== PROJECT EXTRACTION TEST =====")

for project in resume_data.projects:

    print("\nProject Name:")
    print(project.name)

    print("Technologies:")
    print(project.technologies)

    print("Description:")
    print(project.description)