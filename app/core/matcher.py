# matcher.py
# Matches a candidate profile against job listings
# Uses MPNet embeddings + cosine similarity

from sklearn.metrics.pairwise import cosine_similarity
from app.core.embedder import candidate_to_text, job_to_text, get_embedding
import time



# MAIN MATCHING FUNCTION


def match_jobs(candidate: dict, jobs: list, top_n: int = 10) -> list:
    """
    Matches a candidate against all jobs and returns
    the top N most relevant jobs ranked by score.

    Args:
        candidate : candidate profile dictionary
        jobs      : list of job dictionaries
        top_n     : number of top results to return

    Returns:
        List of jobs sorted by match score (highest first)
    """
    print(f"  Matching candidate: {candidate.get('job_title')}...")
    start = time.time()

    # Step 1 — Embed the candidate profile
    candidate_text   = candidate_to_text(candidate)
    candidate_vector = get_embedding(candidate_text)

    # Step 2 — Embed each job and calculate similarity
    results = []

    for job in jobs:

        # Skip jobs with no title or description
        if not job.get("title") or not job.get("description"):
            continue

        # Embed the job
        job_text   = job_to_text(job)
        job_vector = get_embedding(job_text)

        # Calculate cosine similarity score
        score = cosine_similarity(
            candidate_vector.reshape(1, -1),
            job_vector.reshape(1, -1)
        )[0][0]

        # Store result
        results.append({
            "title"        : job.get("title", ""),
            "company"      : job.get("company", "Unknown"),
            "location"     : job.get("location", ""),
            "score"        : round(float(score), 4),
            "score_percent": f"{round(float(score) * 100, 2)}%",
            "url"          : job.get("url", "")
        })

    # Step 3 — Sort by score highest to lowest
    results.sort(key=lambda x: x["score"], reverse=True)

    elapsed = round(time.time() - start, 2)
    print(f"  Done in {elapsed}s — Top score: {results[0]['score_percent']}")

    return results[:top_n]