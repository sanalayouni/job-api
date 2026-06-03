# main.py
# FastAPI entry point for Job API
# Model: all-mpnet-base-v2 (selected )

from fastapi import FastAPI
from app.api.routes import router


# 1. CREATE APP


app = FastAPI(
    title       = "Job API",
    description = """
## AI-Powered Job Matching API

Matches candidate profiles against real job listings using
**MPNet** (all-mpnet-base-v2) — selected after comparing
3 models in our experiment notebook.

## Endpoints
- POST /jobs/refresh      — fetch fresh jobs from Adzuna
- POST /jobs/match        — match a candidate to jobs

## Model
- **all-mpnet-base-v2** — best accuracy in our evaluation
- See `notebook/experiment.ipynb` for full comparison
    """,
    version = "2.0.0"
)


# REGISTER ROUTES


app.include_router(router, prefix="/jobs")

# ROOT

@app.get("/")
def root():
    return {
        "message"  : "Welcome to Job API",
        "version"  : "2.0.0",
        "model"    : "all-mpnet-base-v2",
        "docs"     : "/docs",
        "endpoints": {
            "refresh": "POST /jobs/refresh",
            "match"  : "POST /jobs/match"
        }
    }