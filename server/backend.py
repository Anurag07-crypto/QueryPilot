import sys
from pathlib import Path

# Add parent directory to path to allow imports from work_space
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from work_space.agent import my_agent
# ///////////////////////////////////////////////
class QueryRequest(BaseModel):
    query:str
app = FastAPI(title="morden_rag")
@app.post("/chat")
def chat(request: QueryRequest):
    answer = my_agent(request.query)

    return {"response": answer}
if __name__ == "__main__":
    
    uvicorn.run("backend:app", port=8000, host="127.0.0.1", reload=True)