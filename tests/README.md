# LegalLens Comprehensive Test Suite

This directory contains the automated test suite for both the backend (Django REST Framework) and frontend (Next.js / React) of the LegalLens application.

---

## Folder Structure

```
tests/
├── README.md                          # Test suite documentation
├── run_tests.py                       # Unified test runner for backend and frontend
├── backend/                           # Backend Django unit & API integration tests
│   ├── pytest.ini                     # Pytest configuration
│   ├── conftest.py                    # Fixtures (API Client, PDF generator, DB mocks)
│   ├── test_pdf_service.py            # PII masking & PDF chunking tests
│   ├── test_gemini_service.py         # AI prompts, JSON parsing & error handling tests
│   ├── test_vector_service.py         # Vector embedding & chunk search tests
│   ├── test_upload_view.py            # API test for POST /api/upload/
│   ├── test_chat_view.py              # API test for POST /api/chat/
│   └── test_compare_view.py           # API test for POST /api/compare/
└── frontend/                          # Frontend React & API client tests
    ├── package.json                   # Test runner dependencies (Vitest, RTL, JSDOM)
    ├── vite.config.ts                 # Vitest configuration & module aliases
    ├── setupTests.ts                  # Testing Library setup
    ├── lib/
    │   └── api.test.ts                # API client wrapper tests (upload, chat, compare)
    └── components/
        ├── Navbar.test.tsx            # Navbar brand title tests
        ├── RiskBadge.test.tsx         # Severity badges (High/Medium/Low) tests
        ├── DiffMatrix.test.tsx        # Contract diff matrix & empty state tests
        ├── FileUploader.test.tsx      # Dropzone, file limit validation & loading state tests
        └── ChatInterface.test.tsx     # Message exchange & Q&A interaction tests
```

---

## How to Run Tests

### 1. Run Unified Test Suite (Backend + Frontend)

To execute all backend and frontend tests together:

```bash
python tests/run_tests.py
```

---

### 2. Run Backend Tests Only

Navigate to the `tests/backend` directory and run `pytest`:

```bash
cd tests/backend
pytest -v
```

---

### 3. Run Frontend Tests Only

First, install dependencies in `tests/frontend` if running for the first time:

```bash
cd tests/frontend
npm.cmd install
```

To run all frontend tests:

```bash
npm.cmd test
```

To run tests in watch mode during development:

```bash
npm.cmd run test:watch
```
