from fastapi import FastAPI

app = FastAPI(title="DevDesk", version="0.1.0")


@app.get("/")
def home():
    return {
        "name": "DevDesk",
        "message": "Welcome to DevDesk!",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
