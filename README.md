# 🖥️ DevDesk

> A full-stack developer productivity workspace built with Python, FastAPI, SQLite, HTML, CSS and JavaScript.

[![CI](https://github.com/OmTalekarDev/DevDesk/actions/workflows/ci.yml/badge.svg)](https://github.com/OmTalekarDev/DevDesk/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## ✨ Features

- 📊 Dashboard with live productivity statistics and a 7-day activity chart
- 🔐 Registration, login, bearer-token sessions and logout
- ✅ User-scoped task CRUD: create, read, update, complete and delete
- 🔎 Client-side task search
- 📝 Quick notes stored locally in the browser
- ✦ Optional AI developer assistant through an OpenAI-compatible API
- 🩺 Health endpoint and automatic FastAPI docs
- 🧪 API tests with pytest
- ⚙️ GitHub Actions CI on pushes and pull requests
- 🐳 Docker-ready deployment configuration

## 🧱 Architecture

```text
Browser
  │
  ├── HTML / CSS / JavaScript
  │
  ▼
FastAPI
  ├── Authentication & sessions
  ├── Task REST API
  ├── Productivity statistics
  └── Optional AI provider
  │
  ▼
SQLite
  ├── users
  ├── sessions
  └── tasks
```

## 📁 Project Structure

```text
DevDesk/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── ai.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── schemas_auth.py
│   ├── stats.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── tests/
│   └── test_api.py
├── .github/workflows/ci.yml
├── Dockerfile
├── render.yaml
├── .env.example
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

```bash
git clone https://github.com/OmTalekarDev/DevDesk.git
cd DevDesk
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and create an account.

API docs: `http://127.0.0.1:8000/docs`

### Environment

Copy `.env.example` to your own environment configuration. Never commit real API keys.

For the optional AI assistant, configure:

```text
AI_API_URL=<OpenAI-compatible chat completions endpoint>
AI_API_KEY=<your secret>
AI_MODEL=<model name>
```

## 🔌 API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health/status check |
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Create a session |
| POST | `/auth/logout` | Revoke a session |
| GET | `/auth/me` | Current user |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List current user's tasks |
| GET | `/tasks/{id}` | Get one task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/stats` | Productivity statistics |
| POST | `/ai/ask` | Ask the configured AI provider |

## 🧪 Tests & CI

Run locally:

```bash
pytest -q
```

Every push to `main` and pull request runs the test suite through GitHub Actions.

## 🐳 Docker

```bash
docker build -t devdesk .
docker run -p 8000:8000 devdesk
```

`render.yaml` provides a deployment starting point for Render.

> **Production note:** SQLite is excellent for a portfolio/single-instance app. For multi-instance production deployment, move persistent data to PostgreSQL and use a managed secret store.

## 🛣️ Roadmap

- [x] FastAPI foundation
- [x] SQLite database
- [x] User authentication
- [x] Task CRUD
- [x] Dashboard UI
- [x] Productivity statistics
- [x] AI provider integration
- [x] Automated tests + CI
- [x] Docker deployment setup
- [ ] Server-side notes API
- [ ] PostgreSQL production storage
- [ ] Public deployment

## 🧠 Skills Demonstrated

`Python` `FastAPI` `REST API` `SQLite` `Pydantic` `Authentication` `JavaScript` `HTML` `CSS` `Docker` `GitHub Actions` `AI Integration`

---

Built by **Om Talekar** · `OmTalekarDev`
