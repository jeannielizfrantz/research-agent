from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class Query(BaseModel):
    topic: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/research")
def research(query: Query):
    result = run_agent(query.topic)
    return {"result": result}
