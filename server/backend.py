import sys
from pathlib import Path

# Add parent directory to path to allow imports from work_space
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from work_space.agent import my_agent
from work_space.logger import get_logger

logger = get_logger(__name__)

class QueryRequest(BaseModel):
    """Request schema for the /chat endpoint."""
    
    query: str
app = FastAPI(title="modern_rag")
@app.post("/chat")
def chat(request: QueryRequest):
    """Handle incoming chat queries through the RAG pipeline.

    Args:
        request (QueryRequest): QueryRequest object containing the user query

    Raises:
        HTTPException: On runtime or unexpected errors

    Returns:
        Dict with 'response' key containing the agent's answer
    """
    
    logger.info(f"Incoming query: {request.query[:50]}...")
    try:
        answer = my_agent(request.query)
        logger.info("Query answered successfully")
        return {"response": answer}
    except RuntimeError as e:
        logger.error(f"Runtime error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. please try again"
        )
if __name__ == "__main__":
    
    uvicorn.run("backend:app", port=8000, host="127.0.0.1", reload=True)
