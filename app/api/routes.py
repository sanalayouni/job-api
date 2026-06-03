# routes.py
# Clean API endpoints using MPNet (best model from experiment)
# 3 endpoints: health, refresh jobs, match candidate

from fastapi import APIRouter, HTTPException
from app.core.matcher import match_jobs
from app.services.adzuna import load_jobs, fetch_jobs, save_jobs

router = APIRouter()


# ENDPOINT 1 : REFRESH JOBS


@router.post("/refresh")
def refresh_jobs(query: str = "Python developer", pages: int = 2):
    """
    Fetches fresh jobs from Adzuna and saves locally.
    Call this to update the job database.

    Args:
        query : search keyword (default: Python developer)
        pages : pages to fetch, each page = 50 jobs
    """
    try:
        jobs = fetch_jobs(query=query, pages=pages)
        save_jobs(jobs)
        return {
            "status"    : "ok",
            "message"   : f"Fetched and saved {len(jobs)} jobs",
            "total_jobs": len(jobs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ENDPOINT 2 : MATCH CANDIDATE


@router.post("/match")
def match_candidate(candidate: dict, top_n: int = 10):
    """
    Matches a candidate profile against all jobs.
    Uses MPNet — the best model from our experiment.

    Args:
        candidate : candidate profile sent by the backend team
        top_n     : number of top matches to return (default 10)

    Expected candidate format:
        {
            "job_title"       : "Python Backend Developer",
            "skills"          : ["Python", "Django", "REST APIs"],
            "location"        : "Tunisia",
            "experience_years": 2,
            "summary"         : "Optional summary text"
        }
    """
    try:
        # Validate candidate has at least a job title
        if not candidate.get("job_title"):
            raise HTTPException(
                status_code=400,
                detail="candidate must have a job_title"
            )

        # Load jobs from local file
        jobs = load_jobs()

        if not jobs:
            raise HTTPException(
                status_code=404,
                detail="No jobs found. Call /api/jobs/refresh first."
            )

        # Run matching
        results = match_jobs(candidate, jobs, top_n=top_n)

        return {
            "candidate"            : candidate.get("job_title"),
            "model"                : "all-mpnet-base-v2",
            "total_jobs_evaluated" : len(jobs),
            "top_matches"          : results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))