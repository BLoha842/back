from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="React FastAPI App")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели
class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    completed: bool = False
    created_at: Optional[datetime] = None

class User(BaseModel):
    username: str
    message: str

# Хранилище
tasks_db = {}
messages_db = []

# API Endpoints
@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return list(tasks_db.values())

@app.post("/api/tasks", response_model=Task)
def create_task(task: Task):
    task.id = str(uuid.uuid4())
    task.created_at = datetime.now()
    tasks_db[task.id] = task
    return task

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task.id = task_id
    tasks_db[task_id] = task
    return task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return {"message": "Task deleted"}

@app.post("/api/messages")
def add_message(user: User):
    messages_db.append(user)
    return {"message": f"Hello {user.username}, your message: {user.message}"}

@app.get("/api/messages")
def get_messages():
    return messages_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)