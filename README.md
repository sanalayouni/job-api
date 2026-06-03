# Job — AI-Powered Job Matching API


> Match candidate profiles to real job listings using semantic AI embeddings.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat&logo=fastapi)
![MPNet](https://img.shields.io/badge/Model-MPNet-orange?style=flat&logo=huggingface)
![Adzuna](https://img.shields.io/badge/Jobs-Adzuna_API-purple?style=flat)
![License](https://img.shields.io/badge/License-Educational-lightgrey?style=flat)

---

## What Is Job?

Job is an **AI-powered REST API** that matches a candidate profile against real job listings using **semantic embeddings** — not keyword matching.

Instead of looking for exact words, it understands the **meaning** behind skills and job titles:

```
"Python Developer"   ≈   "Backend Engineer"       → high match
"Python Developer"   ≈   "Chef"                   → low match
```

---

## How It Works

```
1. Candidate profile is sent to the API
         ↓
2. MPNet converts it into a vector (768 numbers)
         ↓
3. MPNet converts each job listing into a vector
         ↓
4. Cosine similarity compares candidate vs each job
         ↓
5. Jobs are ranked by relevance score
         ↓
6. Top matches returned as JSON
```

---

## Model Selection

Before building the API, we ran a **full experiment** comparing 3 models:

| Model | Top Score | Speed | Selected |
|---|---|---|---|
| `all-MiniLM-L6-v2` | 72.48% | Fast (4s) | |
| `all-mpnet-base-v2` | **77.90%** | Moderate (79s) |  **Winner** |
| `paraphrase-multilingual-MiniLM-L12-v2` | 73.86% | Moderate (85s) | |

**MPNet** was selected for its superior accuracy.
Full experiment available in `notebook/experiment.ipynb`.

---

## Project Structure

```
jobbridge-api/
│
├── app/                        # Main application
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── embedder.py         # MPNet model & text conversion
│   │   └── matcher.py          # Matching & ranking logic
│   └── services/
│       ├── __init__.py
│       └── adzuna.py           # Adzuna API integration
│
├── notebook/
│   └── experiment.ipynb        # Model comparison & evaluation
│
├── data/
│   └── jobs_processed.json     # Fetched job listings
│
├── run.py                      # Start the server
├── requirements.txt            # Dependencies
├── .env.example                # Environment variables template
├── .gitignore
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **MPNet** (all-mpnet-base-v2) | Semantic embedding model |
| **Sentence Transformers** | Model loading & inference |
| **Cosine Similarity** | Vector comparison |
| **Adzuna API** | Real job listings source |
| **Plotly** | Interactive visualizations (notebook) |
| **Pandas** | Evaluation metrics (notebook) |

---

## API Endpoints

### `POST /jobs/refresh`
Fetch fresh job listings from Adzuna and save locally.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | `Python developer` | Job search keyword |
| `pages` | integer | `2` | Pages to fetch (1 page = 50 jobs) |

**Response:**
```json
{
  "status": "ok",
  "message": "Fetched and saved 100 jobs",
  "total_jobs": 100
}
```
<img width="1157" height="843" alt="Capture d&#39;écran 2026-06-03 020856" src="https://github.com/user-attachments/assets/561c613a-f1ff-48a8-97c8-ff846161fcd9" />
---

### `POST /jobs/match`
Match a candidate profile against all jobs in the database.

**Request Body:**
```json
{
  "job_title": "Python Backend Developer",
  "skills": ["Python", "Django", "REST APIs", "PostgreSQL"],
  "location": "Tunisia",
  "experience_years": 2,
  "summary": "Optional short description"
}
```

| Field | Required | Description |
|---|---|---|
| `job_title` | ✅ Yes | Candidate's job title |
| `skills` | ✅ Yes | List of technical skills |
| `location` | ✅ Yes | Candidate's location |
| `experience_years` | ❌ Optional | Years of experience |
| `summary` | ❌ Optional | Short bio or description |

**Response:**
```json
{
  "candidate": "Python Backend Developer",
  "model": "all-mpnet-base-v2",
  "total_jobs_evaluated": 100,
  "top_matches": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Paris, France",
      "score": 0.7790,
      "score_percent": "77.9%",
      "url": "https://www.adzuna.fr/..."
    }
  ]
}
```
<img width="1190" height="834" alt="Capture d&#39;écran 2026-06-03 021000" src="https://github.com/user-attachments/assets/220187b7-8ce9-418f-a799-aad05f44b192" />

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sanalayouni/job-api.git
cd job-api
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Open .env and fill in your Adzuna credentials
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
ADZUNA_COUNTRY=fr
ADZUNA_RESULTS_PER_PAGE=50
```

> Get a free Adzuna API key at [developer.adzuna.com](https://developer.adzuna.com)

### 5. Start the Server
```bash
python run.py
```

### 6. Open the API Docs
```
http://127.0.0.1:8000/docs
```

---

## Quick Start (After Installation)

```bash
# Step 1 — Fetch jobs
POST /jobs/refresh
query = "Python developer"
pages = 2

# Step 2 — Match your candidate
POST /jobs/match
{
  "job_title": "Python Backend Developer",
  "skills": ["Python", "Django", "REST APIs", "PostgreSQL"],
  "location": "Tunisia",
  "experience_years": 2
}
```

---

## Experiment Notebook

The `notebook/experiment.ipynb` contains the full model evaluation:

- Loads all 3 candidate models
- Runs matching with each model
- Evaluates using: Top Score, Top 5 Average, Top 10 Average, Coverage
- Generates 5 interactive Plotly visualizations
- Concludes with model selection

**To run the notebook:**
```bash
jupyter notebook
# Open notebook/experiment.ipynb
# Run all cells
```

---

## Why Adzuna?

| Option | Legal | Free | API |
|---|---|---|---|
| **Adzuna** | ✅ | ✅ | ✅ |
| LinkedIn | ❌ | ✅ | ❌ |
| Indeed | ❌ | ✅ | ❌ |
| Glassdoor | ❌ | ✅ | ❌ |

Scraping platforms like LinkedIn violates their Terms of Service.
Adzuna provides an **official, free, and reliable API** — the right choice for a production-ready system.

---

## Future Improvements

- Add database (PostgreSQL) to replace JSON storage
- Support multiple candidates at once
- Add skill weighting system
- Add experience level filtering
- Build a web dashboard (React or Streamlit)
- Deploy to cloud (Railway, Render, or AWS)

---

## Author

**Sana Layouni**
Built as part of the HireNest team project.

---

## License

This project is for educational and research purposes.
