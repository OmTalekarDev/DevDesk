# 🖥️ DevDesk

> A developer productivity dashboard built with Python, FastAPI, and SQLite.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## 🎯 Goal

DevDesk is a portfolio project for building a practical web application from the ground up. It combines a Python API, persistent data, and a developer-focused dashboard.

## 🚧 Current Status

**Phase 1 — Backend foundation**

- ✅ FastAPI application initialized
- ✅ Health endpoint added
- ✅ Dependency file added
- ✅ Python package structure added
- ⏳ SQLite data layer
- ⏳ Tasks and notes API
- ⏳ Frontend dashboard
- ⏳ Authentication
- ⏳ AI assistant features

## 📁 Project Structure

```text
DevDesk/
├── app/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Run Locally

```bash
git clone https://github.com/OmTalekarDev/DevDesk.git
cd DevDesk
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

Interactive API docs: `http://127.0.0.1:8000/docs`

## 🔌 Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | DevDesk status and welcome message |
| GET | `/health` | Service health check |

## 🛣️ Roadmap

- [x] FastAPI foundation
- [x] Health check
- [ ] SQLite database
- [ ] CRUD API for tasks
- [ ] Notes API
- [ ] Search
- [ ] Dashboard UI
- [ ] Authentication
- [ ] Productivity statistics
- [ ] AI-powered developer assistant
- [ ] Deployment

## 🧠 Skills

`Python` `FastAPI` `REST API` `SQLite` `HTML` `CSS` `JavaScript` `Git` `Linux` `AI`

---

Built by **Om Talekar** · `OmTalekarDev`
