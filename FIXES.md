# FIXES.md

This document details every bug found in the original source code, including the file, line number, what the problem was, and how it was fixed.

---

## API — `api/main.py`

| # | File | Line | Problem | Fix |
|---|---|---|---|---|
| 1 | `api/main.py` | 6 | Redis hardcoded to `localhost` | Replaced with `os.getenv("REDIS_HOST")` |
| 2 | `api/main.py` | N/A | No `/health` endpoint | Added `/health` route returning `{"status": "ok"}` |
| 3 | `api/main.py` | 9-10 | Job pushed to queue before status set — race condition | Set status to `queued` before `lpush` |
| 4 | `api/main.py` | 16-17 | Missing job returns HTTP 200 instead of 404 | Raised `HTTPException(status_code=404)` |
| 5 | `api/main.py` | 1 | `HTTPException` used but never imported | Added to FastAPI import line |
| 6 | `api/main.py` | 32 | Unnecessary `if __name__ == "__main__"` block | Removed — uvicorn started via Dockerfile CMD |
| 7 | `api/main.py` | 13,20,27,29,30 | Flake8 errors: E302, E231, W391 | Added blank lines, whitespace after colons, removed trailing blank line |

---

## Worker — `worker/worker.py`

| # | File | Line | Problem | Fix |
|---|---|---|---|---|
| 8 | `worker/worker.py` | 5 | Redis hardcoded to `localhost` | Replaced with `os.getenv("REDIS_HOST")` |
| 9 | `worker/worker.py` | 7-11 | No error handling — one bad job crashes worker permanently | Wrapped in try/except, sets status to `failed` on error |
| 10 | `worker/worker.py` | 7-11 | Job status skips `processing` state | Added `r.hset` to set status to `processing` before work begins |
| 11 | `worker/worker.py` | 4 | `signal` imported but never used — lint failure and no graceful shutdown | Implemented SIGTERM and SIGINT handlers |
| 12 | `worker/worker.py` | N/A | No healthcheck signal for Docker | Added heartbeat file write to `/tmp/worker_healthy` on every loop |
| 13 | `worker/worker.py` | 12,23,31,32,33,35 | Flake8 errors: E302, E305, W191, E101, E117 | Added blank lines, replaced tabs with spaces |

---

## Frontend — `frontend/package.json`

| # | File | Line | Problem | Fix |
|---|---|---|---|---|
| 14 | `frontend/package.json` | 4, 7 | Entry point referenced `app.js` which doesn't exist | Changed `main` and `start` script to `server.js` |

---

## Frontend — `frontend/server.js`

| # | File | Line | Problem | Fix |
|---|---|---|---|---|
| 15 | `frontend/server.js` | 5 | API URL hardcoded to `http://localhost:8000` | Replaced with `process.env.API_URL || "http://api:8000"` |
