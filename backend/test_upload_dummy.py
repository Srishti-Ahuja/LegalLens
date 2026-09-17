import requests, json, os

API_URL = "http://localhost:8000/api"

pdf_path = r"e:/Projects/New folder/LegalAssistant/backend/dummy.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF not found at {pdf_path}")

# Upload PDF
with open(pdf_path, "rb") as f:
    files = {"file": f}
    upload_resp = requests.post(f"{API_URL}/upload/", files=files)
    print("Upload status:", upload_resp.status_code)
    upload_json = upload_resp.json()
    print("Upload response:", json.dumps(upload_json, indent=2))

# If succeeded, ask a question
if upload_resp.ok and "document_id" in upload_json:
    doc_id = upload_json["document_id"]
    query = "What is the main topic of the document?"
    chat_resp = requests.post(f"{API_URL}/chat/", json={"query": query, "document_id": doc_id})
    print("Chat status:", chat_resp.status_code)
    print("Chat response:", json.dumps(chat_resp.json(), indent=2))
else:
    print("Upload failed, cannot query.")
