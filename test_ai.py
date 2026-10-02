from ai_engine.client import client


response = client.responses.create(
    model="gpt-5-mini",
    input="Say hello to IntelliInterview in one short sentence."
)

print("===== AI RESPONSE =====")
print(response.output_text)