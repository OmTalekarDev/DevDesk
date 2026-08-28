from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .ai import ask_ai
from .auth import authenticate, create_session, create_user, delete_session, get_user_by_token, init_auth_db
from .database import init_db
from .models import create_task, delete_task, get_task, list_tasks, update_task
from .schemas import Task, TaskCreate, TaskUpdate
from .schemas_auth import AIRequest, AuthRequest
from .stats import productivity_stats

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_auth_db()
    yield


app = FastAPI(title="DevDesk", version="2.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    user = get_user_by_token(authorization.split(" ", 1)[1].strip())
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return user


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "database": "sqlite", "version": "2.0.0"}


@app.post("/auth/register", status_code=201)
def register(payload: AuthRequest):
    try:
        user = create_user(payload.username, payload.password)
    except Exception as exc:
        if "UNIQUE" in str(exc).upper():
            raise HTTPException(status_code=409, detail="Username already exists") from exc
        raise
    token, expires_at = create_session(user["id"])
    return {"user": user, "token": token, "expires_at": expires_at}


@app.post("/auth/login")
def login(payload: AuthRequest):
    user = authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token, expires_at = create_session(user["id"])
    return {"user": user, "token": token, "expires_at": expires_at}


@app.post("/auth/logout")
def logout(authorization: str | None = Header(default=None)):
    if authorization and authorization.lower().startswith("bearer "):
        delete_session(authorization.split(" ", 1)[1].strip())
    return {"message": "Logged out"}


@app.get("/auth/me")
def me(user: dict = Depends(current_user)):
    return user


@app.post("/tasks", response_model=Task, status_code=201)
def add_task(payload: TaskCreate, user: dict = Depends(current_user)):
    return create_task(payload.title, payload.description, user["id"])


@app.get("/tasks", response_model=list[Task])
def get_tasks(user: dict = Depends(current_user)):
    return list_tasks(user["id"])


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, user: dict = Depends(current_user)):
    task = get_task(task_id, user["id"])
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, payload: TaskUpdate, user: dict = Depends(current_user)):
    task = update_task(task_id, user["id"], payload.title, payload.description, payload.completed)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, user: dict = Depends(current_user)):
    if not delete_task(task_id, user["id"]):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted", "id": task_id}


@app.get("/stats")
def stats(user: dict = Depends(current_user)):
    return productivity_stats(user["id"])


@app.post("/ai/ask")
async def ai_ask(payload: AIRequest, user: dict = Depends(current_user)):
    try:
        answer = await ask_ai(payload.prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI provider error: {exc}") from exc
    return {"answer": answer}
