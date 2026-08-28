from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .database import init_db
from .models import create_task, delete_task, get_task, list_tasks, update_task
from .schemas import Task, TaskCreate, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="DevDesk", version="0.2.0", lifespan=lifespan)


@app.get("/")
def home():
    return {"name": "DevDesk", "message": "Developer dashboard API", "status": "online"}


@app.get("/health")
def health():
    return {"status": "ok", "database": "sqlite"}


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
