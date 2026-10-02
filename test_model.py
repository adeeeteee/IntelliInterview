from models.resume import ResumeData


resume = ResumeData(
    name="Adithi Bhrugubanda",
    email="adithi@example.com",
    education=["B.E. Information Science and Engineering"],
    skills=["Python", "Java", "SQL", "FastAPI"],
    projects=["IntelliInterview", "Honeypot Log Analyser"],
    experience=[],
    certifications=["Python Certification"]
)


print("===== RESUME DATA =====")
print(resume)