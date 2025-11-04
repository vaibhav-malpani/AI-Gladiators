# AI Gladiators

Turn natural language prompts into AI-driven gladiators, then pit them against each other in simulated battles. This repository contains:
- A FastAPI backend for fighter management and battle simulation
- A React + Vite frontend for creating fighters, running battles, and viewing rankings
- A simple game engine and AI agent with optional Google Gemini integration


## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Setup](#setup)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (React + Vite)](#frontend-react--vite)
- [Run](#run)
- [API Endpoints](#api-endpoints)
- [Scripts](#scripts)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Roadmap / TODOs](#roadmap--todos)


## Overview
AI Gladiators lets you describe a fighter in natural language. The backend parses the description (optionally using Google Gemini) to generate a fighter profile with stats, traits, and preferred moves. Fighters are persisted to JSON files and can be matched against each other in simulated battles. The frontend provides a modern interface to manage fighters and view battle results.


## Tech Stack
- Backend: Python, FastAPI, Pydantic, Uvicorn
- Frontend: React 18, Vite, React Router, Tailwind CSS
- AI (optional): Google Gemini via `google-generativeai`
- Config: `.env` via `python-dotenv`
- Data storage: Local JSON files under `data/`


## Requirements
- Python 3.9+ (recommended)
- Node.js 18+ and npm (Vite 5 requires Node 18 or newer)
- OS: Windows/macOS/Linux


## Project Structure
```
AI Gladiator/
├─ api/
│  ├─ data/
│  │  └─ fighters/                # Example fighter JSON files (runtime data is under ./data/)
│  └─ main.py                      # FastAPI app entry (module: api.main:app)
├─ frontend/
│  ├─ src/                         # React app sources
│  ├─ vite.config.js               # Dev server config (port 5173, proxy /api -> http://localhost:8000)
│  └─ package.json                 # Frontend scripts
├─ game/
│  ├─ ai_agent.py                  # AI agent (Gemini integration fallback to rule-based)
│  ├─ battle_engine.py             # Battle simulation logic
│  ├─ fighter.py                   # Fighter model
│  └─ fighter_manager.py           # Persistence and retrieval
├─ requirements.txt                # Python dependencies
├─ .env                            # Example environment variables (do not commit real secrets)
└─ README.md
```

Note: At runtime the backend also ensures these folders exist at the repository root:
```
./data/
./data/fighters/
./data/battles/
```


## Environment Variables
Create a `.env` file in the project root (see provided `.env` example). Key variables:

Backend:
- `ENVIRONMENT` (e.g., `development`)
- `DEBUG` (`True`/`False`)
- `SECRET_KEY` (set a strong value in production)
- `DATABASE_URL` (optional; defaults to SQLite file path)
- `API_HOST` (default `0.0.0.0`)
- `API_PORT` (default `8000`)
- `MAX_HEALTH`, `MAX_STAMINA`, `ROUNDS_PER_BATTLE` (game tuning)
- `AI_TEMPERATURE`, `AI_MAX_TOKENS` (AI generation tuning)
- `LOG_LEVEL`, `LOG_FILE`
- `GOOGLE_GEMINI_API_KEY` (optional: enables Gemini)
- `GOOGLE_PROJECT_ID`, `GOOGLE_LOCATION` (optional/future use)

Frontend (Vite):
- `VITE_API_URL` (e.g., `http://localhost:8000`)
- `VITE_WS_URL` (if websockets are used; e.g., `ws://localhost:8000/ws`)

Security note: Never commit real API keys or secrets to source control.


## Setup

### Backend (FastAPI)
1. Create and activate a virtual environment
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux (bash):
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create and configure `.env` at the repo root (copy from `.env` provided and adjust as needed).

4. Run the API with Uvicorn (development):
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open API docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc


### Frontend (React + Vite)
1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```
   Vite runs at http://localhost:5173 and proxies `/api` calls to `http://localhost:8000`.

3. Configure `.env` at repo root with `VITE_API_URL` if your API is not on the default.


## Run
Open two terminals:
- Terminal A (backend):
  ```bash
  uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
  ```
- Terminal B (frontend):
  ```bash
  cd frontend
  npm run dev
  ```

Build frontend for production:
```bash
cd frontend
npm run build
npm run preview   # optional local preview
```


## API Endpoints
Base URL (dev): `http://localhost:8000`

- `GET /` – Root info (service banner, version, docs link)
- `GET /api/fighters` – List all fighters
- `GET /api/fighters/{fighter_id}` – Get a fighter by ID
- `POST /api/fighters` – Create a fighter from a natural language prompt
  - Body: `{ "prompt": "string (>= 10 chars)" }`
- `DELETE /api/fighters/{fighter_id}` – Delete a fighter by ID
- `POST /api/battle` – Simulate a battle between two fighters
  - Body: `{ "fighter1_id": "uuid", "fighter2_id": "uuid" }`
- `POST /api/train/{fighter_id}` – Train a fighter (improves stats)
- `GET /api/rankings` – Get fighter rankings (wins/losses/level)
- `GET /api/stats` – Global stats

Interactive docs: http://localhost:8000/docs


## Scripts

Backend (run directly with Uvicorn):
- Dev: `uvicorn api.main:app --reload`

Frontend (`frontend/package.json`):
- `npm run dev` – Start Vite dev server
- `npm run build` – Build for production
- `npm run preview` – Preview local production build
- `npm run lint` – Lint source files


## Testing
- Currently no automated tests are included.
- TODO: Add unit tests for `game/` modules (battle outcomes, damage calc, AI decisions) and API route tests (FastAPI `TestClient`).

Example future commands:
```bash
# after adding pytest to requirements
pytest -q
```


## Troubleshooting
- Gemini not used / AI fallback:
  - Ensure `GOOGLE_GEMINI_API_KEY` is set in `.env`. Without it, the app uses a rule-based fallback (still works).
- CORS/Proxy issues in frontend:
  - Vite dev proxy forwards `/api` to `http://localhost:8000`. Make sure the backend is running on that port.
- Data not persisting:
  - The backend saves fighters under `./data/fighters/`. Ensure the process has write permissions and the working directory is the repo root.
- Windows PowerShell execution policy:
  - If activating venv fails, start PowerShell as Administrator and run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.


## Roadmap / TODOs
- [ ] Add automated tests for backend and game engine
- [ ] Add Dockerfile/docker-compose for unified dev environment
- [ ] Add CI (lint + tests)
- [ ] Persist data in a database for production
- [ ] Expand AI capabilities and training loops (Vertex AI integration)
- [ ] Write detailed contribution guidelines
