from fastapi import FastAPI
from pydantic import BaseModel
from agent import process_text
from db import save_tasks

class InputText(BaseModel):
    text: str

app = FastAPI()

@app.post("/generate")
def generate_tasks(payload: InputText):
    tasks = process_text(payload.text)
    save_tasks(tasks)
    return tasks
