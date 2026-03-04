# Push to GitHub and host for free

## 1. Push this repo to your GitHub (sid776)

**Prerequisites:** Git installed and signed in (or use GitHub Desktop).

### Option A: Command line

```bash
cd c:\Users\siddh\Downloads\WB_POC

git init
git add .
git commit -m "Document Intelligence POC - World Bank VPU dashboard and API"

# Create repo on GitHub first: https://github.com/new → name: WB_POC → Create (no README)
git remote add origin https://github.com/sid776/WB_POC.git
git branch -M main
git push -u origin main
```

If the repo **WB_POC** already exists under https://github.com/sid776, create it empty (no README, no .gitignore), then run the commands above.

### Option B: GitHub Desktop

1. File → Add local repository → choose `c:\Users\siddh\Downloads\WB_POC` (if it says "not a Git repository", create one there first).
2. Publish repository → choose your account (sid776), name: **WB_POC**, then Publish.

---

## 2. Host for free

### A. Streamlit Community Cloud (dashboard only, recommended)

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Sign in with GitHub (sid776).
3. Click **New app** → select repo **sid776/WB_POC**, branch **main**.
4. **Main file path:** `dashboard.py`
5. **Advanced settings** → Python version: 3.11 (or 3.10).
6. Deploy. You’ll get a URL like `https://wb-poc-dashboard-xxx.streamlit.app`.

**Note:** This runs only the dashboard (World Bank data + fallback). The Document Intelligence API (RAG) runs locally; the live "vector store" count will show only when you run the API locally.

### B. Render (API + dashboard, free tier)

1. Go to [render.com](https://render.com), sign in with GitHub.
2. **New → Web Service** → connect **sid776/WB_POC**.
3. Build: **pip install -r requirements.txt**
4. Start: **python run_api.py** (or **uvicorn app.main:app --host 0.0.0.0 --port $PORT**).
5. Create a second **Web Service** for the dashboard: Start command **streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0**.

Free tier spins down after inactivity; first load may be slow.

### C. Railway (free tier)

1. [railway.app](https://railway.app) → Login with GitHub → New project.
2. Deploy from GitHub repo **sid776/WB_POC**.
3. Set start command for API: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add another service for the dashboard: `streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0`.

---

**Quick path:** Push to GitHub, then deploy the **dashboard** on [Streamlit Community Cloud](https://share.streamlit.io) with main file `dashboard.py` for a live public URL in a few minutes.
