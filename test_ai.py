from app.services.ai_service import ai_service

response = ai_service.generate(
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    temperature=1
)

print(response)