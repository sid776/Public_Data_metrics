# Free hosting — Push to GitHub & deploy

## 1. Push this project to GitHub

From the project root (`WB_POC`), run in **PowerShell** or **Command Prompt**:

```powershell
cd c:\Users\siddh\Downloads\WB_POC

# Initialize repo (only if not already a git repo)
git init

# Add the GitHub remote (repo: https://github.com/sid776/Public_Data_metrics)
git remote add origin https://github.com/sid776/Public_Data_metrics.git
# If remote already exists, update it:
# git remote set-url origin https://github.com/sid776/Public_Data_metrics.git

# Stage all files (respects .gitignore)
git add .

# Commit
git commit -m "World Bank Document Intelligence POC: dashboard, RAG API, MLflow"

# Use main branch and push (if repo is empty, this creates main)
git branch -M main
git push -u origin main
```

If GitHub asks for auth, use a **Personal Access Token** (Settings → Developer settings → Personal access tokens) as the password, or sign in with **GitHub CLI** (`gh auth login` then `git push`).

---

## 2. Host the dashboard for free — Streamlit Community Cloud

[Streamlit Community Cloud](https://share.streamlit.io/) offers free hosting for Streamlit apps connected to a GitHub repo.

### Steps

1. Go to **https://share.streamlit.io/** and sign in with GitHub.
2. Click **“New app”**.
3. **Repository:** `sid776/Public_Data_metrics`  
   **Branch:** `main`  
   **Main file path:** `dashboard.py`
4. Click **“Deploy!”**.

Streamlit will install dependencies from `requirements.txt` and run:

```bash
streamlit run dashboard.py
```

Your app will get a URL like:  
`https://<your-app-name>.streamlit.app`

### Optional: config

- The app uses port **8501** by default on Community Cloud (no need to set `--server.port`).
- To use a custom theme or title, keep `.streamlit/config.toml` in the repo (it’s already there).

### Notes

- **World Bank API:** The dashboard calls the public World Bank API; no API key needed. It works from Streamlit’s servers.
- **Document Intelligence API:** The “Live” status and vector store count only work when the FastAPI backend is running. On Community Cloud you only deploy the dashboard; the backend would need to be hosted separately (e.g. Render, Railway) if you want that.
- **Free tier:** Community Cloud has usage limits; for a demo/POC it’s usually enough.

---

## 3. Other free hosting options

| Service | Use case |
|--------|----------|
| [Streamlit Community Cloud](https://share.streamlit.io/) | Best for this Streamlit dashboard; connect GitHub and deploy. |
| [Hugging Face Spaces](https://huggingface.co/spaces) | Run the app in a Space (choose “Streamlit” as SDK). |
| [Render](https://render.com) | Free tier for web services; can run both FastAPI and Streamlit (separate services). |
| [Railway](https://railway.app) | Free tier; good for API + dashboard with a bit more setup. |

For “push and host the dashboard with minimal setup,” use **Streamlit Community Cloud** and the steps in section 2.
