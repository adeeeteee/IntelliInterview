from resume_parser.parser import extract_text_from_pdf


file_path = "AdithiBhrugubanda_resume.pdf"

text = extract_text_from_pdf(file_path)

print("===== EXTRACTED RESUME TEXT =====")
print(text)