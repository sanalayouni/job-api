import nbformat as nbf
import os

os.makedirs("notebook", exist_ok=True)

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    return nbf.v4.new_markdown_cell(text)

def code(text):
    return nbf.v4.new_code_cell(text)


# CELL 1 - Title
cells.append(md("# JobBridge - Model Experiment & Evaluation\n\n**Goal:** Compare 3 AI models for job matching, evaluate each one, and pick the best for production.\n\n| Phase | Description |\n|---|---|\n| 1 | Load jobs & candidate profile |\n| 2 | Run all 3 models |\n| 3 | Evaluate results |\n| 4 | Visualize with Plotly |\n| 5 | Conclude & pick the best model |"))


# CELL 2 - Imports
cells.append(md("## Step 1 - Imports & Setup"))
cells.append(code(
"import sys\n"
"import os\n"
"import time\n"
"import pandas as pd\n"
"import plotly.graph_objects as go\n"
"from plotly.subplots import make_subplots\n"
"\n"
"# Add root to path so we can import our modules\n"
"sys.path.append(os.path.dirname(os.getcwd()))\n"
"\n"
"from app.core.embedder import MODELS, load_model, candidate_to_text, job_to_text, get_embedding\n"
"from app.core.matcher import match_with_model\n"
"from app.services.adzuna import load_jobs\n"
"\n"
"print('All imports successful')"
))


# CELL 3 - Candidate & Jobs
cells.append(md("## Step 2 - Candidate Profile & Jobs"))
cells.append(code(
"CANDIDATE = {\n"
"    'job_title'       : 'Python Backend Developer',\n"
"    'skills'          : ['Python', 'Django', 'REST APIs', 'PostgreSQL'],\n"
"    'location'        : 'Tunisia',\n"
"    'experience_years': 2\n"
"}\n"
"\n"
"jobs = load_jobs()\n"
"\n"
"print('Candidate  :', CANDIDATE['job_title'])\n"
"print('Skills     :', ', '.join(CANDIDATE['skills']))\n"
"print('Location   :', CANDIDATE['location'])\n"
"print('Experience :', CANDIDATE['experience_years'], 'years')\n"
"print()\n"
"print('Jobs loaded:', len(jobs))\n"
"print()\n"
"print('Sample jobs:')\n"
"for job in jobs[:3]:\n"
"    print(' -', job['title'], '@', job['company'], '--', job['location'])"
))


# CELL 4 - Run all 3 models
cells.append(md("## Step 3 - Run All 3 Models\n\nWe run the candidate profile against all jobs using each model and record match scores and execution time."))
cells.append(code(
"all_results = {}\n"
"timing      = {}\n"
"\n"
"for model_name in MODELS:\n"
"    print('Running', model_name, '...')\n"
"    start = time.time()\n"
"\n"
"    results = match_with_model(CANDIDATE, jobs, model_name)\n"
"\n"
"    elapsed = round(time.time() - start, 2)\n"
"    all_results[model_name] = results\n"
"    timing[model_name]      = elapsed\n"
"\n"
"    print('  Done in', elapsed, 'seconds')\n"
"    print('  Top 3 matches:')\n"
"    for i, job in enumerate(results[:3], 1):\n"
"        print('   ', i, '.', job['title'], '->', job['score_percent'])\n"
"    print()\n"
"\n"
"print('All models finished!')"
))


# CELL 5 - Evaluation Table
cells.append(md("## Step 4 - Evaluation\n\nWe evaluate each model using:\n- **Top Score** - highest match score\n- **Top 5 Average** - average of top 5 scores\n- **Top 10 Average** - average of top 10 scores\n- **Jobs above 60%** - strong matches\n- **Jobs above 50%** - decent matches\n- **Speed** - how fast the model runs"))
cells.append(code(
"rows = []\n"
"\n"
"for model_name, results in all_results.items():\n"
"    scores = [r['score'] for r in results]\n"
"    rows.append({\n"
"        'Model'       : model_name,\n"
"        'Top Score %' : round(scores[0] * 100, 2),\n"
"        'Top 5 Avg %' : round(sum(scores[:5])  / 5  * 100, 2),\n"
"        'Top 10 Avg %': round(sum(scores[:10]) / 10 * 100, 2),\n"
"        'Jobs >= 60%' : sum(1 for s in scores if s >= 0.60),\n"
"        'Jobs >= 50%' : sum(1 for s in scores if s >= 0.50),\n"
"        'Speed (s)'   : timing[model_name]\n"
"    })\n"
"\n"
"df = pd.DataFrame(rows)\n"
"\n"
"print('=' * 65)\n"
"print('MODEL EVALUATION SUMMARY')\n"
"print('=' * 65)\n"
"print(df.to_string(index=False))\n"
"print('=' * 65)\n"
"print()\n"
"print('WINNER BY CATEGORY:')\n"
"print('  Best Accuracy :', df.loc[df['Top Score %'].idxmax(),  'Model'])\n"
"print('  Best Average  :', df.loc[df['Top 5 Avg %'].idxmax(),  'Model'])\n"
"print('  Fastest       :', df.loc[df['Speed (s)'].idxmin(),    'Model'])\n"
"print('  Best Coverage :', df.loc[df['Jobs >= 60%'].idxmax(),  'Model'])"
))


# CELL 6 - Chart 1: Top Scores
cells.append(md("## Step 5 - Visualizations\n\n### Chart 1 - Top Score per Model"))
cells.append(code(
"colors = ['#3B82F6', '#10B981', '#F59E0B']\n"
"models = df['Model'].tolist()\n"
"scores = df['Top Score %'].tolist()\n"
"\n"
"fig1 = go.Figure(data=[\n"
"    go.Bar(\n"
"        x            = models,\n"
"        y            = scores,\n"
"        marker_color = colors,\n"
"        text         = [str(s) + '%' for s in scores],\n"
"        textposition = 'outside',\n"
"        width        = 0.4\n"
"    )\n"
"])\n"
"\n"
"fig1.update_layout(\n"
"    title       = 'Top Match Score by Model',\n"
"    xaxis_title = 'Model',\n"
"    yaxis_title = 'Top Score (%)',\n"
"    yaxis       = dict(range=[0, 100]),\n"
"    template    = 'plotly_white',\n"
"    height      = 420\n"
")\n"
"\n"
"fig1.show()"
))


# CELL 7 - Chart 2: Average Scores
cells.append(md("### Chart 2 - Average Scores (Top 5 vs Top 10)"))
cells.append(code(
"fig2 = go.Figure(data=[\n"
"    go.Bar(\n"
"        name         = 'Top 5 Average',\n"
"        x            = df['Model'],\n"
"        y            = df['Top 5 Avg %'],\n"
"        marker_color = '#3B82F6',\n"
"        text         = [str(v) + '%' for v in df['Top 5 Avg %']],\n"
"        textposition = 'outside'\n"
"    ),\n"
"    go.Bar(\n"
"        name         = 'Top 10 Average',\n"
"        x            = df['Model'],\n"
"        y            = df['Top 10 Avg %'],\n"
"        marker_color = '#10B981',\n"
"        text         = [str(v) + '%' for v in df['Top 10 Avg %']],\n"
"        textposition = 'outside'\n"
"    )\n"
"])\n"
"\n"
"fig2.update_layout(\n"
"    title       = 'Average Scores - Top 5 vs Top 10',\n"
"    xaxis_title = 'Model',\n"
"    yaxis_title = 'Average Score (%)',\n"
"    yaxis       = dict(range=[0, 100]),\n"
"    barmode     = 'group',\n"
"    template    = 'plotly_white',\n"
"    height      = 420\n"
")\n"
"\n"
"fig2.show()"
))


# CELL 8 - Chart 3: Speed vs Accuracy
cells.append(md("### Chart 3 - Speed vs Accuracy Tradeoff"))
cells.append(code(
"colors     = ['#3B82F6', '#10B981', '#F59E0B']\n"
"models     = list(all_results.keys())\n"
"speeds     = [timing[m] for m in models]\n"
"top_scores = [round(all_results[m][0]['score'] * 100, 2) for m in models]\n"
"\n"
"fig3 = go.Figure()\n"
"\n"
"for i, model in enumerate(models):\n"
"    fig3.add_trace(go.Scatter(\n"
"        x            = [speeds[i]],\n"
"        y            = [top_scores[i]],\n"
"        mode         = 'markers+text',\n"
"        name         = model,\n"
"        text         = [model],\n"
"        textposition = 'top center',\n"
"        marker       = dict(size=22, color=colors[i])\n"
"    ))\n"
"\n"
"fig3.update_layout(\n"
"    title       = 'Speed vs Accuracy Tradeoff',\n"
"    xaxis_title = 'Time (seconds) - lower is better',\n"
"    yaxis_title = 'Top Score (%) - higher is better',\n"
"    template    = 'plotly_white',\n"
"    height      = 450\n"
")\n"
"\n"
"fig3.show()"
))


# CELL 9 - Chart 4: Score Distribution
cells.append(md("### Chart 4 - Score Distribution per Model"))
cells.append(code(
"colors = ['#3B82F6', '#10B981', '#F59E0B']\n"
"fig4   = go.Figure()\n"
"\n"
"for i, (model_name, results) in enumerate(all_results.items()):\n"
"    scores = [round(r['score'] * 100, 2) for r in results]\n"
"    fig4.add_trace(go.Box(\n"
"        y            = scores,\n"
"        name         = model_name,\n"
"        marker_color = colors[i],\n"
"        boxpoints    = 'all',\n"
"        jitter       = 0.3,\n"
"        pointpos     = -1.8\n"
"    ))\n"
"\n"
"fig4.update_layout(\n"
"    title       = 'Score Distribution per Model',\n"
"    yaxis_title = 'Match Score (%)',\n"
"    template    = 'plotly_white',\n"
"    height      = 450\n"
")\n"
"\n"
"fig4.show()"
))


# CELL 10 - Chart 5: Top Jobs per Model
cells.append(md("### Chart 5 - Top 5 Jobs per Model"))
cells.append(code(
"colors = ['#3B82F6', '#10B981', '#F59E0B']\n"
"\n"
"fig5 = make_subplots(\n"
"    rows           = 1,\n"
"    cols           = 3,\n"
"    subplot_titles = list(all_results.keys()),\n"
"    shared_yaxes   = False\n"
")\n"
"\n"
"for col, (model_name, results) in enumerate(all_results.items(), 1):\n"
"    top5   = results[:5]\n"
"    titles = [\n"
"        r['title'][:25] + '...' if len(r['title']) > 25\n"
"        else r['title']\n"
"        for r in top5\n"
"    ]\n"
"    scores = [round(r['score'] * 100, 2) for r in top5]\n"
"\n"
"    fig5.add_trace(\n"
"        go.Bar(\n"
"            x            = scores,\n"
"            y            = titles,\n"
"            orientation  = 'h',\n"
"            marker_color = colors[col - 1],\n"
"            text         = [str(s) + '%' for s in scores],\n"
"            textposition = 'outside',\n"
"            name         = model_name\n"
"        ),\n"
"        row=1, col=col\n"
"    )\n"
"\n"
"fig5.update_layout(\n"
"    title      = 'Top 5 Job Matches per Model',\n"
"    template   = 'plotly_white',\n"
"    height     = 500,\n"
"    showlegend = False\n"
")\n"
"\n"
"fig5.show()"
))


# CELL 11 - Conclusion
cells.append(md("## Step 6 - Conclusion & Model Selection"))
cells.append(code(
"best_accuracy = df.loc[df['Top Score %'].idxmax(),  'Model']\n"
"best_avg      = df.loc[df['Top 5 Avg %'].idxmax(),  'Model']\n"
"best_speed    = df.loc[df['Speed (s)'].idxmin(),    'Model']\n"
"best_coverage = df.loc[df['Jobs >= 60%'].idxmax(),  'Model']\n"
"\n"
"print('=' * 55)\n"
"print('EXPERIMENT CONCLUSION')\n"
"print('=' * 55)\n"
"print('Best Accuracy :', best_accuracy)\n"
"print('Best Average  :', best_avg)\n"
"print('Fastest       :', best_speed)\n"
"print('Best Coverage :', best_coverage)\n"
"print('=' * 55)\n"
"print()\n"
"print('SELECTED MODEL FOR PRODUCTION:', best_accuracy)\n"
"print()\n"
"print('Reason:')\n"
"print('  - Highest top score')\n"
"print('  - Best average across top matches')\n"
"print('  - Most relevant results for Python Backend roles')\n"
"print()\n"
"print('This model will be hardcoded in the API.')\n"
"print('=' * 55)"
))


# Save notebook
nb.cells = cells
path = "notebook/experiment.ipynb"
with open(path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook created at:", path)
print("Now run: jupyter notebook")
print("Then open: experiment.ipynb")