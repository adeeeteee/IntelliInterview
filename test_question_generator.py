from resume_parser.parser import extract_text_from_pdf
from resume_parser.section_splitter import split_resume_sections
from ai_engine.resume_extractor import extract_resume_data
from ai_engine.question_generator import generate_questions


file_path = "AdithiBhrugubanda_resume.pdf"

resume_text = extract_text_from_pdf(file_path)

sections = split_resume_sections(resume_text)

resume_data = extract_resume_data(
    resume_text,
    sections
)

questions = generate_questions(resume_data)

print("\n===== GENERATED INTERVIEW QUESTIONS =====")
print(questions)