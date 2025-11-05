Aqarino™ — Local Setup (Tunisian Theme)
======================================

Goal:
- Run Aqarino locally to test the AI agent, widget, and integration before deploying to client websites.
- This package is product-ready and branded with the Aqarino™ trademark. Do not remove the trademark from the widget.

Prerequisites (on your machine):
- Python 3.10+ installed
- Node.js (only if you plan to build a custom frontend) — optional
- Git (optional, for versioning)
- (Optional) Docker & docker-compose if you want containerized run

Quick start (Linux/macOS):
1. Unzip this package and open a terminal in the project root.
2. Copy env example:
   cp .env.example .env
   Then edit .env with your API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.).
3. Create a Python virtualenv and install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
4. Run the backend server (FastAPI via Uvicorn):
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
5. Open the demo frontend in your browser:
   http://localhost:8000/static/host/aqarino-widget-tn.umd.js
   Or open the demo page: frontend/demo/index.html (you can open the file directly or serve it with a static server)

Windows (PowerShell):
1. Copy .env.example to .env and edit.
2. python -m venv .venv
3. .\.venv\Scripts\Activate.ps1
4. pip install -r backend/requirements.txt
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Notes:
- The widget is injected from /static/host/aqarino-widget-tn.umd.js. Keep the path when embedding on client sites.
- For production, replace the placeholder widget with your production build file, preserving the Aqarino™ trademark per licensing.
- If you want me to prepare a client-installable package (one file installer or npm package for the widget), say the word and I’ll prepare it.

