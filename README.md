# Smart Guard

Smart Guard is a production-grade security monitoring platform that combines a Python-based backend with a modern Vite + React frontend. The project provides real-time video stream analysis, event processing, administrative dashboards, and integration points for notifications and storage.

**Highlights**
- **Real-time video analytics:** Stream processing and event detection via backend workers.
- **Modern frontend:** Responsive dashboard and monitoring UI built with Vite and React.
- **Extensible architecture:** Clear separation between services, workers, and UI for easier customization and deployment.

**Repository Layout**
- `SmartGuard/Backend` — FastAPI services, background workers, configuration, and Python dependencies.
- `SmartGuard/Frontend` — Vite + React application and frontend assets.
- `ENVIRONMENT_SETUP.md` — Notes and environment-specific setup guidance.

**Requirements**
- Python 3.9+ (for the backend)
- Node.js 16+ and npm or Yarn (for the frontend)
- Git
- Docker (recommended for containerized deployment)

**Quick Start — Backend (Local)**
1. Create and activate a virtual environment:

```bash
python -m venv .venv
# PowerShell (Windows)
.venv\\Scripts\\Activate.ps1
# Command Prompt (Windows)
.venv\\Scripts\\activate.bat
```

2. Install dependencies and run the backend:

```bash
pip install -r SmartGuard/Backend/requirements.txt
python SmartGuard/Backend/main.py
```

Notes:
- Use `SmartGuard/Backend/start_backend.py` if you require the included startup wrapper.
- Check `SmartGuard/Backend/config/settings.py` for environment-specific configuration values.

**Quick Start — Frontend (Local)**
1. Install dependencies and start the development server:

```bash
cd SmartGuard/Frontend
npm install
npm run dev
```

2. Build production assets:

```bash
npm run build
```

**Configuration**
- Environment-specific settings are located in `SmartGuard/Backend/config/settings.py`.
- Provide secrets (API keys, database URLs, Twilio credentials, etc.) via environment variables or a secrets manager; do not commit secrets to the repository.

**Docker**
- A Docker image for the backend is recommended for production. Create a `Dockerfile` in `SmartGuard/Backend` and use the standard build/push workflow to publish to a container registry.

**CI / CD (Suggested)**
- Frontend: GitHub Actions to build assets and deploy to GitHub Pages, Netlify, or an S3/CloudFront pipeline.
- Backend: Build and publish a Docker image to GitHub Container Registry (GHCR) or Docker Hub, then deploy to your cloud provider (e.g., ECS, Kubernetes, DigitalOcean App Platform).

I can add example GitHub Actions workflows for both frontend and backend — tell me if you want GitHub Pages and GHCR specifically.

**Development Guidelines**
- Create feature branches off `main` using clear, descriptive names.
- Keep commits small and focused; use PRs for review and CI validation.

**Contributing**
Contributions are welcome. Please open issues to discuss significant changes before submitting pull requests.

**License & Contact**
- Repository: https://github.com/AhmedSaad332/SmartGuard
- For questions or commercial licensing inquiries, open an issue or contact the repository owner.

