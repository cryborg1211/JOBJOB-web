## JobJob Web — React + Vite (Tailwind v4) & Flask API

This repo contains a Vite React frontend styled with Tailwind v4 and a Flask backend for candidate profiles with avatar upload and SQLite persistence.

### Prerequisites

- Node.js ≥ 18, npm ≥ 9
- Python ≥ 3.10 (Windows: tested on 3.13)

### Project structure (top-level)

```
server/                 # Flask API
  app.py               # API endpoints (candidates CRUD)
  db.py                # SQLAlchemy setup
  models.py            # Candidate model
  uploads/avatars/     # Saved avatar images (served as /uploads/avatars/...)
  requirements.txt
src/                    # React app
  lib/config.js        # API_BASE config
  pages/
    CandidateNew.jsx
    CandidateReviewFromServer.jsx
    LandingPage.jsx
    RoleSelect.jsx
vite.config.js
```

### Backend — Flask API

1) Create and activate a virtual environment

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\activate
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Run API (with CORS enabled and SQLite auto-created)

```powershell
python app.py
# → http://127.0.0.1:5000
```

The API exposes:

- POST `/api/candidates` (multipart/form-data)
  - fields: `name, degree, languages (comma-separated), exp1, exp2, skill1, skill2`
  - file: `avatar` (.png/.jpg/.jpeg, ≤ 5MB)
  - returns created candidate JSON with `id` and `avatar_url`

- GET `/api/candidates/:id`

- PUT `/api/candidates/:id` (multipart or JSON)
  - same fields as POST; include `avatar` file to change avatar

Notes:

- Images stored under `server/uploads/avatars/` and served at `/uploads/avatars/<file>`
- Database file: `server/app.db` (SQLite)

### Frontend — React + Vite + Tailwind v4

1) Install deps

```powershell
npm install
```

2) Configure API base (optional)

Create `.env.local` in project root (same level as `package.json`) if you need a custom API URL:

```
VITE_API_BASE=http://127.0.0.1:5000
```

Otherwise, it defaults to `http://127.0.0.1:5000` (see `src/lib/config.js`).

3) Run dev server

```powershell
npm run dev
# → http://localhost:5173
```

Main routes:

- `/` — landing page
- `/trial` — role selection
- `/candidate/new` — create profile (avatar upload + fields)
- `/candidate/review/:id` — view and edit saved profile (fetches from API)

### Typical dev workflow

1) Terminal A — backend:

```powershell
cd server
.\.venv\Scripts\activate
python app.py
```

2) Terminal B — frontend:

```powershell
npm run dev
```

3) In the browser:

```
/trial → ỨNG VIÊN → /candidate/new → fill form + upload avatar → XÁC NHẬN
→ redirect to /candidate/review/:id (server data) → CHỈNH SỬA → LƯU
```

### Production build (frontend)

```powershell
npm run build
npm run preview
```

### Notes & decisions

- Tailwind v4 is enabled via `@tailwindcss/vite`; no tailwind.config is used. `src/index.css` only contains `@import "tailwindcss";`.
- The legacy CV scanning flow has been removed. Any old debug scripts now print a deprecation message.
- If you run into Windows path issues, ensure you use PowerShell with the venv activated.

### Troubleshooting

- Avatar upload rejected:
  - Ensure the file is `.png/.jpg/.jpeg` and ≤ 5MB.
- 404 on `/uploads/avatars/...`:
  - Confirm `server/uploads/avatars/` exists and Flask is running; the API serves that folder statically.
- DB not created:
  - `init_db(app)` creates tables on startup; check `server/app.db` permissions.

### License

Internal project. © Your Company.

# jobjob-web
Test
