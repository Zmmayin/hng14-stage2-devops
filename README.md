# Job Processing System

A job processing system made up of three services — a frontend, an API, and a worker — all containerized with Docker and orchestrated with Docker Compose.

---

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

| Tool | Version | Installation |
|---|---|---|
| Docker | 24.0+ | https://docs.docker.com/get-docker/ |
| Docker Compose | 2.0+ | Included with Docker Desktop |
| Git | Any | https://git-scm.com/downloads |

Verify your installations:
```bash
docker --version
docker compose version
git --version
```

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/Zmmayin/hng14-stage2-devops.git
cd hng14-stage2-devops
```

---

## Step 2 — Create your Environment File

```bash
cp .env.example .env
```

The default values in `.env.example` work out of the box for local development. You do not need to change anything to get started.

---

## Step 3 — Bring the Full Stack Up

```bash
docker compose up --build -d
```

This command will:
- Build all three service images from their Dockerfiles
- Start Redis, the API, the Worker, and the Frontend
- Each service will only start after its dependency is confirmed healthy

---

## Step 4 — Verify All Services are Running

```bash
docker compose ps
```

Expected output:
```
NAME       STATUS
redis      Up (healthy)
api        Up (healthy)
worker     Up (healthy)
frontend   Up (healthy)
```

---

## What a Successful Startup Looks Like

### Check the frontend is serving
```bash
curl http://localhost:3000
```
Expected: Frontend HTML page loads successfully.

### Submit a job
```bash
curl -X POST http://localhost:3000/submit
```
Expected response:
```json
{"job_id": "some-uuid-here"}
```

### Check job status
```bash
curl http://localhost:3000/status/some-uuid-here
```
Expected response:
```json
{"job_id": "some-uuid-here", "status": "completed"}
```

### Check service logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs api
docker compose logs worker
docker compose logs frontend
```

Worker logs should show:
```
Processing job some-uuid-here
Done: some-uuid-here
```

### Check API health directly
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status": "ok"}
```

---

## Stopping the Stack

```bash
# Stop all services
docker compose down

# Stop and remove all volumes
docker compose down -v
```

---

## Project Structure

```
hng14-stage2-devops/
├── .github/
│   └── workflows/
│       └── pipeline.yml      # CI/CD pipeline
├── api/
│   ├── Dockerfile
│   ├── main.py               # FastAPI application
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       └── test_main.py      # Unit tests
├── worker/
│   ├── Dockerfile
│   └── worker.py             # Job processing worker
├── frontend/
│   ├── Dockerfile
│   ├── server.js             # Express frontend server
│   └── package.json
├── docker-compose.yml
├── .env.example
├── FIXES.md
└── README.md
```

---

## CI/CD Pipeline

The pipeline runs automatically on every push and pull request to `main`. It runs the following stages in strict order:

| Stage | Description |
|---|---|
| Lint | Checks Python (flake8), JavaScript (eslint), and Dockerfiles (hadolint) |
| Test | Runs pytest unit tests for the API with Redis mocked |
| Build | Builds all images and pushes to local registry tagged with git SHA |
| Security Scan | Scans all images with Trivy, fails on CRITICAL vulnerabilities |
| Integration Test | Brings full stack up, submits a job, polls until completed |
| Deploy | Runs on `main` only — rolling update with health check verification |

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `API_URL` | API URL for frontend | `http://api:8000` |
| `FRONTEND_PORT` | Port to expose frontend on | `3000` |

---

## Troubleshooting

**Services not starting:**
```bash
docker compose logs
```

**Redis not healthy:**
```bash
docker exec redis redis-cli ping
# Expected: PONG
```

**Job stuck on queued:**
```bash
docker compose logs worker
# Check worker is running and connected to Redis
```

**API not reachable:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```
