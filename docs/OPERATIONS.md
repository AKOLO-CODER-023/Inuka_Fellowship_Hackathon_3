# Operations Manual

Covers running, monitoring, and recovering the Inuka Supply Chain system.
Written for whoever picks up support after the hackathon (Em-Tech / KPC
IT), so it says what's actually true about this build today rather than
an idealised future state.

## What's Running

Two services, one shared codebase:

| Service | What it is | Port | Health check |
|---|---|---|---|
| Backend API | FastAPI app (`backend/main.py`) | 8000 | `GET /health` |
| Dashboard | Streamlit app (`dashboard/app.py`) | 8501 | `GET /_stcore/health` |

Both read from the same `data/` CSVs. The backend additionally writes to
a local SQLite file (`backend/inuka.db`) to persist replenishment
decisions.

## Running It

**Locally, without Docker:**
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload          # terminal 1
streamlit run dashboard/app.py                        # terminal 2
```

**With Docker (recommended for the demo — matches what CI builds):**
```bash
docker compose up --build
```
Backend docs at `http://localhost:8000/docs`, dashboard at `http://localhost:8501`.

## Environment Variables

| Variable | Required? | Purpose |
|---|---|---|
| `SLACK_WEBHOOK_URL` | No | If set, `backend/alerts.py` posts CRITICAL/HIGH risk alerts to this Slack Incoming Webhook. If unset, alerts are still logged, just not posted anywhere external. |

No other secrets or credentials are required — everything else runs
against local files and a local SQLite database.

## Monitoring

- `GET /health` reports `"healthy"` only if **both** the database and
  the forecast data file are reachable — not just if the process is up.
  Point your uptime monitor here, not at `/`.
- Every request and error is logged to stdout with a timestamp and
  level (`backend/main.py` configures this at import time). In Docker,
  `docker compose logs -f backend` tails it live.
- CRITICAL/HIGH-risk replenishment decisions additionally log at
  `WARNING`/`CRITICAL` level via `backend/alerts.py`, and optionally to
  Slack if `SLACK_WEBHOOK_URL` is set.

## Known Limitations (be honest about these in the demo Q&A)

- **No trained forecasting model is committed yet.** `/forecast` falls
  back to a data-driven naive 7-day baseline computed from
  `data/forecasting_features.csv`. It's real data, not a placeholder
  number, but it is not the RF/XGBoost/CatBoost comparison the original
  spec called for. Swapping in a trained model bundle
  (`forecasting/model/forecast_model_bundle.pkl`) upgrades this
  automatically — no endpoint code changes needed.
- **No production database.** SQLite is fine for a hackathon demo; it
  is not sized for concurrent production writes. A real deployment
  should move `backend/database.py` to Postgres before going live.
- **Alerting is log-based by default.** Slack posting only activates if
  someone sets `SLACK_WEBHOOK_URL`. There is no PagerDuty integration.
- **No load testing has been done.** Response times under real KPC
  request volume are unknown.

## Disaster Recovery

- **State that matters:** `backend/inuka.db` (replenishment decision
  history) is the only stateful, non-regenerable data the backend
  produces. Everything else (CSVs in `data/`, code) is version-controlled.
- **If the backend crashes or the container is lost:** redeploy from
  the `main` branch via CI. A fresh SQLite file is created automatically
  on startup (`initialize_database()` in `backend/database.py`) — you
  lose decision history, not the ability to run.
- **If you need to preserve decision history across redeploys:** mount
  `backend/inuka.db` on a persistent volume rather than baking it into
  the container image (the current `Dockerfile.backend` does not do
  this — it's a hackathon-speed default, flagged here deliberately).
- **If `data/` CSVs are corrupted or lost:** they're checked into the
  repo, so `git checkout -- data/` restores the last-known-good version.

## Support Handover Checklist

- [ ] Rotate/set a real `SLACK_WEBHOOK_URL` for the receiving team's own
      Slack workspace.
- [ ] Move SQLite to a persistent-volume-backed instance or a managed
      Postgres before any real operational use.
- [ ] Confirm CI (`.github/workflows/ci.yml`) is passing on `main` before
      handover, and that receiving team has repo access to see it run.
- [ ] Walk the receiving team through `GET /health` and what "degraded"
      vs "healthy" means operationally.
- [ ] Agree who owns replacing the naive baseline forecast with a
      trained model, and by when.
