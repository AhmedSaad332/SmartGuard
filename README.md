# Smart Guard

Smart Guard is a security monitoring platform with a Python backend and a Vite/React frontend. This repository contains the full project (Backend + Frontend).

**Quick Overview**
- Backend: Python FastAPI-based services and workers (directory: `SmartGuard/Backend`).
- Frontend: Vite + React app (directory: `SmartGuard/Frontend`).

**Prerequisites**
- Python 3.9+ (recommended) and `venv`
- Node.js 16+ and npm/yarn
- Git (already used to push this repo)

**Backend — Local run**
1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat
```

2. Install requirements and run:

```bash
pip install -r SmartGuard/Backend/requirements.txt
python SmartGuard/Backend/main.py
# or
python SmartGuard/Backend/start_backend.py
```

**Frontend — Local run**
1. Install dependencies and start dev server:

```bash
cd SmartGuard/Frontend
npm install
npm run dev
```

2. Build for production:

```bash
npm run build
```

**Repository structure (top-level)**
- `SmartGuard/Backend` — backend app, requirements, workers and config
- `SmartGuard/Frontend` — Vite/React frontend
- `ENVIRONMENT_SETUP.md` — environment notes
- `.gitignore` — ignores for local envs and build artifacts

**CI / Deployment**
- I can add GitHub Actions to build and deploy the frontend to GitHub Pages and publish backend Docker images to GitHub Container Registry. Ask me to add those workflows and I'll create them.

**Contributing**
- Open an issue or create a branch and submit a PR.

**Contact**
- Repository: https://github.com/AhmedSaad332/SmartGuard

