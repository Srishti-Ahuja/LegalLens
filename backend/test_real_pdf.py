import requests, os, json

API_URL = "http://localhost:8000/api"

# 1. Download a sample PDF with text
pdf_url = "https://www.africau.edu/images/default/sample.pdf"
pdf_path = "sample_text.pdf"
resp = requests.get(pdf_url)
if resp.status_code == 200:
    with open(pdf_path, "wb") as f:
        f.write(resp.content)
    print("Downloaded sample PDF (size", len(resp.content), "bytes)")
else:
    raise Exception(f"Failed to download PDF: {resp.status_code}")

# 2. Upload the PDF
with open(pdf_path, "rb") as f:
    files = {"file": f}
    upload_resp = requests.post(f"{API_URL}/upload/", files=files)
    print("Upload status:", upload_resp.status_code)
    upload_json = upload_resp.json()
    print("Upload response:", json.dumps(upload_json, indent=2))

# 3. If upload succeeded, ask a question
if upload_resp.ok and "document_id" in upload_json:
    doc_id = upload_json["document_id"]
    query = "What is the main topic of the document?"
    chat_resp = requests.post(f"{API_URL}/chat/", json={"query": query, "document_id": doc_id})
    print("Chat status:", chat_resp.status_code)
    print("Chat response:", json.dumps(chat_resp.json(), indent=2))
else:
    print("Upload failed, skipping chat test.")
