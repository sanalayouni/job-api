# adzuna.py
# Handles all communication with the Adzuna Jobs API
# Fetches real job listings and saves them locally

import httpx
import json
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# CONFIGURATION

APP_ID  = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
COUNTRY = os.getenv("ADZUNA_COUNTRY", "fr")
RESULTS = int(os.getenv("ADZUNA_RESULTS_PER_PAGE", 50))

# Adzuna API base URL 
BASE_URL = "https://api.adzuna.com/v1/api/jobs"

# Where to save the fetched jobs
DATA_PATH = "data/jobs_processed.json"



# FETCH JOBS FROM ADZUNA


def fetch_jobs(query: str = "Python developer", pages: int = 2) -> list:
    """
    Fetches job listings from Adzuna API.

    Args:
        query : Job search keyword (e.g. "Python developer")
        pages : Number of pages to fetch (each page = 50 jobs)

    Returns:
        List of cleaned job dictionaries
    """
    all_jobs = []

    for page in range(1, pages + 1):
        print(f"  Fetching page {page}/{pages}...")

        
        url = f"{BASE_URL}/{COUNTRY}/search/{page}"

        # Build request parameters
        params = {
            "app_id"          : APP_ID,
            "app_key"         : APP_KEY,
            "results_per_page": RESULTS,
            "what"            : query,
            "content-type"    : "application/json"
        }

        # Debug — show exactly what we're sending
        print(f"   URL: {url}")

        # Make the API request
        response = httpx.get(url, params=params)

        # Debug — show response status
        print(f"  Status: {response.status_code}")

        # Check if request was successful
        if response.status_code != 200:
            print(f"   Error on page {page}: {response.status_code}")
            print(f"   Response: {response.text[:200]}")  # Show first 200 chars of error
            continue

        # Parse the response
        data = response.json()
        jobs = data.get("results", [])

        # Clean and keep only useful fields
        for job in jobs:
            all_jobs.append({
                "title"      : job.get("title", ""),
                "company"    : job.get("company", {}).get("display_name", "Unknown"),
                "location"   : job.get("location", {}).get("display_name", ""),
                "description": job.get("description", ""),
                "url"        : job.get("redirect_url", "")
            })

    print(f"\n  Total jobs fetched: {len(all_jobs)}")
    return all_jobs



# SAVE JOBS TO LOCAL FILE


def save_jobs(jobs: list) -> None:
    """Saves job list to a local JSON file."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"  Jobs saved to {DATA_PATH}")



# LOAD JOBS FROM LOCAL FILE


def load_jobs() -> list:
    """
    Loads jobs from local file.
    If file doesn't exist, fetches from API first.
    """
    if not os.path.exists(DATA_PATH):
        print("   No local jobs found. Fetching from Adzuna...")
        jobs = fetch_jobs()
        save_jobs(jobs)
    else:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            jobs = json.load(f)
        print(f"  Loaded {len(jobs)} jobs from local file")

    return jobs



# TEST — Run this file directly to test


if __name__ == "__main__":
    print("\n Testing Adzuna Service...")
    print("─" * 40)

    # Check API keys are loaded
    print(f"  APP_ID  : {APP_ID[:4]}****" if APP_ID else "   APP_ID not found in .env")
    print(f"  APP_KEY : {APP_KEY[:4]}****" if APP_KEY else "  APP_KEY not found in .env")
    print(f"  COUNTRY : {COUNTRY}")
    print()

    # Fetch and save jobs
    jobs = fetch_jobs(query="Python developer", pages=2)
    save_jobs(jobs)

    # Show first 3 jobs as preview
    if jobs:
        print("\n Sample jobs fetched:")
        for job in jobs[:3]:
            print(f"  • {job['title']} @ {job['company']} — {job['location']}")
    else:
        print("\n    No jobs returned — check your API keys in .env")