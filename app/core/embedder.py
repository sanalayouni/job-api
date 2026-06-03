# embedder.py
# Loads MPNet — the best model selected from our experiment
# See notebook/experiment.ipynb for the full evaluation

from sentence_transformers import SentenceTransformer
import numpy as np


# BEST MODEL — selected after experiment
# Notebook result: MPNet scored highest
# Model: all-mpnet-base-v2


BEST_MODEL_NAME = "all-mpnet-base-v2"

# Load model once when the app starts
# This avoids reloading on every request
print(f"  Loading model: {BEST_MODEL_NAME}...")
model = SentenceTransformer(BEST_MODEL_NAME)
print(f"  Model ready!")



# CONVERT CANDIDATE PROFILE TO TEXT


def candidate_to_text(candidate: dict) -> str:
    """
    Converts candidate profile into natural language text.
    Richer text = better embeddings = better matches.
    """
    skills  = ", ".join(candidate.get("skills", []))
    summary = candidate.get("summary", "")

    text = (
        f"Job Title: {candidate.get('job_title', '')}. "
        f"Skills: {skills}. "
        f"Experience: {candidate.get('experience_years', '')} years. "
        f"Location: {candidate.get('location', '')}. "
        f"Summary: {summary}"
    )
    return text.strip()



# CONVERT JOB TO TEXT


def job_to_text(job: dict) -> str:
    """
    Converts a job listing into natural language text.
    We use title + company + description (first 300 chars).
    """
    text = (
        f"Job Title: {job.get('title', '')}. "
        f"Company: {job.get('company', '')}. "
        f"Location: {job.get('location', '')}. "
        f"Description: {job.get('description', '')[:300]}"
    )
    return text.strip()



# GENERATE EMBEDDING


def get_embedding(text: str) -> np.ndarray:
    """
    Converts text into a vector using MPNet.

    Args:
        text: any string

    Returns:
        numpy array (768 dimensions for MPNet)
    """
    return model.encode(text, convert_to_numpy=True)