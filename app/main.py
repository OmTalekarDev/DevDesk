from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .models import create_task, delete_task, get_task, list_tasks, update_task
from .schemas import Task, TaskCreate, TaskUpdate

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="DevDesk", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "database": "sqlite", "version": "1.0.0"}


@app.post("/tasks", response_model=Task, status_code=201)
def add_task(payload: TaskCreate):
    return create_task(payload.title, payload.description)


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, payload: TaskUpdate):
    task = update_task(task_id, payload.title, payload.description, payload.completed)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted", "id": task_id}
