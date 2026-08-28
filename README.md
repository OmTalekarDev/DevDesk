# 🖥️ DevDesk

> A full-stack developer productivity workspace built with Python, FastAPI, SQLite, HTML, CSS and JavaScript.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## ✨ Features

- 📊 Developer dashboard with live task statistics
- ✅ Full task CRUD: create, read, update, complete and delete
- 🔎 Client-side task search
- 📝 Quick notes stored in the browser
- 🌙 Responsive dark developer UI
- 🩺 Health endpoint for service monitoring
- 📚 Automatic FastAPI interactive API documentation

## 🧱 Architecture

```text
Browser
  │
  ├── HTML / CSS / JavaScript
  │
  ▼
FastAPI
  │
  ├── Task API
  ├── Validation
  └── Static file server
  │
  ▼
SQLite
  └── tasks
```

## 📁 Project Structure

```text
DevDesk/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Run Locally

```bash
git clone https://github.com/OmTalekarDev/DevDesk.git
cd DevDesk
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the dashboard.

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## 🔌 API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the dashboard |
| GET | `/health` | Health/status check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{id}` | Get one task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## 🛣️ Roadmap

- [x] FastAPI foundation
- [x] SQLite database
- [x] Task CRUD API
- [x] Dashboard UI
- [x] Search
- [x] Quick notes
- [ ] User authentication
- [ ] Server-side notes API
- [ ] Productivity charts
- [ ] AI-powered developer assistant
- [ ] Automated tests and CI
- [ ] Deployment

## 🧠 Skills Demonstrated

`Python` `FastAPI` `REST API` `SQLite` `Pydantic` `HTML` `CSS` `JavaScript` `Git` `Linux`

---

Built by **Om Talekar** · `OmTalekarDev`
