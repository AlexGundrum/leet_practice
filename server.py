from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routers import contests, edge_cases, elo, flashcards, pacing, practice, recommended, specimens

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AlgoRep")
app.include_router(practice.router)
app.include_router(contests.router)
app.include_router(specimens.router)
app.include_router(elo.router)
app.include_router(flashcards.router)
app.include_router(edge_cases.router)
app.include_router(recommended.router)
app.include_router(pacing.router)

# Only these specific repo-root files are servable as static assets. Everything else
# (data/, config/, api/, scripts/, .git/) must never be reachable over HTTP - data/
# holds practice history and config/ holds a Gmail app password once the reminder
# script is set up.
ALLOWED_ROOT_FILES = {
    "worker.js",
    "pyodide.js",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "pyodide-lock.json",
    "python_stdlib.zip",
    "algorithms.json",
}

app.mount("/js", StaticFiles(directory=str(BASE_DIR / "js")), name="js")


@app.get("/")
def serve_index():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/{filename}")
def serve_root_file(filename: str):
    if filename not in ALLOWED_ROOT_FILES:
        raise HTTPException(status_code=404)
    return FileResponse(BASE_DIR / filename)
