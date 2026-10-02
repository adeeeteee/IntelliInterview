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


print("\n===== RESUME DATA OBJECT =====")

print("\nName:")
print(resume_data.name)

print("\nEmail:")
print(resume_data.email)

print("\nEducation:")
print(resume_data.education)

print("\nSkills:")
print(resume_data.skills)

print("\nProjects:")
print(resume_data.projects)

print("\nExperience:")
print(resume_data.experience)

print("\nCertifications:")
print(resume_data.certifications)

print("\n===== DATA TYPE =====")
print(type(resume_data))