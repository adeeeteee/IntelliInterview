from ai_engine.client import ask_ai


prompt = "Explain what an interview is in one simple sentence."

response = ask_ai(prompt)

print("===== AI RESPONSE =====")
print(response)