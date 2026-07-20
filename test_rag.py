from app.services.knowledge_service import knowledge_service

query = "Customer reports duplicate debit card transaction yesterday."

context = knowledge_service.search(query)

print("\nRetrieved Context\n")
print(context)