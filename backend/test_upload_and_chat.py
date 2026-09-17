import requests, json, os

API_URL = "http://localhost:8000/api"

# Step 1: upload test PDF
pdf_path = r"e:/Projects/New folder/LegalAssistant/backend/test_blank.pdf"
with open(pdf_path, "rb") as f:
    files = {"file": f}
    upload_resp = requests.post(f"{API_URL}/upload/", files=files)
    print("Upload response status:", upload_resp.status_code)
    try:
        upload_json = upload_resp.json()
        print("Upload JSON:", upload_json)
    except Exception:
        print("Upload response not JSON:", upload_resp.text)
        raise

# Step 2: if upload succeeded, query the document
if upload_resp.ok and "document_id" in upload_json:
    doc_id = upload_json["document_id"]
    payload = {"query": "What does the document say?", "document_id": doc_id}
    chat_resp = requests.post(f"{API_URL}/chat/", json=payload)
    print("Chat response status:", chat_resp.status_code)
    try:
        print("Chat JSON:", chat_resp.json())
    except Exception:
        print("Chat response not JSON:", chat_resp.text)
else:
    print("Skipping chat test because upload failed.")
