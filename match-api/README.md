match-api

FastAPI service that scores matching between a Job Description (JD) and a CV.

Features
- Downloads model from Kaggle on first run (cached under ./artifacts)
- Two prediction endpoints: raw text and file uploads
- CORS for http://localhost:5173
- 15s request timeout, structured errors, basic rate limiting (60 req/min/IP)
- Dockerfile, Makefile, and tests

Quick start (local)
1) Create .env from example and fill Kaggle credentials or put ~/.kaggle/kaggle.json.
2) Install deps:
```
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```
3) Run dev server:
```
make dev
# or
uvicorn main:app --reload --port 8000
```
4) Open docs: http://localhost:8000/docs

Environment
- KAGGLE_USERNAME, KAGGLE_KEY
- KAGGLE_DATASET (e.g. username/dataset_name) and KAGGLE_FILE (e.g. model.pkl)
- MODEL_LOCAL_PATH default ./artifacts/model.pkl
- SENTENCE_TRANSFORMERS_MODEL optional huggingface model id (e.g. sentence-transformers/all-MiniLM-L6-v2)

Docker
```
make docker-build
make docker-run
```
Container exposes port 8000.

Tests
```
pytest -q
```

