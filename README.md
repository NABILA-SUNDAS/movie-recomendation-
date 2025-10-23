# Backend (FastAPI)

## Quick Start
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run dev server
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Endpoints
- `GET /` → Health check + project info
- `GET /api/search?q=<text>` → Fuzzy search titles
- `GET /api/recommend?title=<movie>&k=10` → Content‑based recommendations
- `GET /api/random?k=12` → Random picks (for the homepage grid)