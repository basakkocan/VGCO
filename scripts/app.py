import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Ensure the scripts directory is in the path
sys.path.append(str(Path(__file__).resolve().parent))
import sparql_translator

# Initialize FastAPI
app = FastAPI(
    title="VGCO Natural Language to SPARQL Interface",
    description="An LLM-powered natural language query interface for the Video Game Catalog Ontology",
    version="1.0"
)

# Global variables
graph = None

@app.on_event("startup")
def startup_event():
    global graph
    print("Loading VGCO ontology graphs into memory...")
    try:
        graph = sparql_translator.load_ontology_graph()
        print(f"Ontology loaded successfully. Total triples: {len(graph)}")
    except Exception as e:
        print(f"Error loading ontology: {e}")
        # We don't crash the server startup, but queries will fail
        graph = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    success: bool
    question: str
    sparql: str = ""
    headers: list = []
    results: list = []
    error: str = ""

@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(payload: QueryRequest):
    global graph
    if graph is None:
        return QueryResponse(
            success=False,
            question=payload.question,
            error="Ontology graph was not loaded successfully on startup."
        )
        
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        sparql_query, headers, rows = sparql_translator.translate_and_query(question, graph)
        return QueryResponse(
            success=True,
            question=question,
            sparql=sparql_query,
            headers=headers,
            results=rows
        )
    except Exception as e:
        return QueryResponse(
            success=False,
            question=question,
            error=str(e)
        )

# Serve Frontend Static Files
repo_root = Path(__file__).resolve().parent.parent
frontend_dir = repo_root / "frontend"

# Check if frontend directory exists, if not create it
if not frontend_dir.exists():
    frontend_dir.mkdir(parents=True, exist_ok=True)

# Mount the static files directory
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/")
async def read_index():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Welcome to VGCO SPARQL API. Frontend index.html not found."}

def main():
    # Make sure env is loaded
    sparql_translator.load_environment()
    port = int(os.getenv("PORT", 8000))
    print(f"Starting VGCO Web Interface on http://localhost:{port}")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()
