# jasonmorrissette.com

Personal portfolio and a documented cloud security engineering case study.

**Stack:** Python 3.13 · FastAPI · Jinja2 · Tailwind CSS v4 · Azure Container Apps · GitHub Actions

## Security highlights

- Strict Content-Security-Policy (no inline scripts or styles, no third-party assets)
- Security headers on every response, including error pages
- CI quality gate: Ruff, Bandit (SAST), pip-audit (SCA), pytest, gitleaks (secret scanning)
- SHA-pinned GitHub Actions with a read-only workflow token

## Local development

```powershell
uv sync
.\bin\tailwindcss.exe -i styles\input.css -o app\static\css\site.css --watch
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
