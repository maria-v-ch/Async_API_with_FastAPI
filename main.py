from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import asyncio

app = FastAPI()

# Dictionary to keep track of tasks
tasks = {}


# BaseModel for task input
class Task(BaseModel):
    duration: int


# Function to simulate a long-running task
async def simulate_task(task_id: str, duration: int):
    await asyncio.sleep(duration)
    tasks[task_id] = "done"


# Endpoint to create a new task
@app.post("/task")
async def create_task(task: Task):
    task_id = str(uuid4())
    tasks[task_id] = "running"
    asyncio.create_task(simulate_task(task_id, task.duration))
    return {"task_id": task_id}


# Endpoint to get task status
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": tasks[task_id]}
