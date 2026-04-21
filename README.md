# Finance Analysis Dashboard

A full-stack financial data pipeline and analysis dashboard that processes market data, generates trading signals, and provides LLM-based insights through an interactive UI.

---

## Live Demo

[https://finance-frontend-pq0l.onrender.com](https://finance-frontend-pq0l.onrender.com)

---

## Overview

This project implements an end-to-end system that:

- Processes OHLCV financial data
- Generates trading signals using deterministic logic
- Computes key metrics (trend, volatility, signal distribution)
- Uses LLMs to interpret results (Groq + OpenRouter)
- Displays insights through a modern React dashboard
- Includes Docker-based deployment for reproducibility

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pandas / NumPy
- LangChain (LCEL)
- Groq API
- OpenRouter API

### Frontend

- React (Vite)
- Axios
- Recharts

### DevOps / Deployment

- Docker & Docker Compose
- Nginx (static serving)
- Render (deployment)

---

## System Architecture

```text
CSV Data
  ↓
Data Processing (pipeline/)
  ↓
Signal Generation (signals.py)
  ↓
Metrics Computation
  ↓
LLM Interpretation (LangChain)
  ↓
FastAPI (/run endpoint)
  ↓
React Frontend (Dashboard + Charts)
```

---

## Features

- Financial metrics (trend, volatility, signal rate)
- Dual LLM analysis (Groq vs OpenRouter)
- Risk and confidence classification
- Interactive price trend chart
- End-to-end pipeline execution via API
- Fully deployable system (Docker + optional cloud)

---

## API Endpoint

`GET /run`

### Example response

```json
{
  "metrics": {},
  "groq_analysis": {},
  "openrouter_analysis": {},
  "chart_data": []
}
```

---

## Local setup

### 1. Clone repository

```bash
git clone https://github.com/13RahulKhanna/finance-analysis-dashboard.git
cd finance-analysis-dashboard
```

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

Run the **API** (used by the frontend):

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Optional: run the **batch CLI** (writes `metrics.json`):

```bash
python main.py --input data.csv --config pipeline/config.yaml --output metrics.json --log-file run.log
```

### 3. Frontend

```bash
cd frontend
npm install
```

Ensure `frontend/.env` points at your local API (included in repo for dev):

```env
VITE_API_URL=http://127.0.0.1:8000/run
```

Start Vite:

```bash
npm run dev
```

Open the URL shown in the terminal (default `http://localhost:5173`).

---

## Docker

```bash
docker compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000) (Nginx serves the SPA; `/api/*` is proxied to the backend)
- Backend: [http://localhost:8000/run](http://localhost:8000/run)

Root `.env` is passed into the **backend** container only (API keys stay off the client bundle).

---

## Deployment

- Backend: Docker on Render (or similar)
- Frontend: Docker image with Nginx + static Vite build
- Production frontend may call a **public** backend URL via `VITE_API_URL` at build time, or same-origin `/api/run` behind a reverse proxy—see `frontend/Dockerfile` and `frontend/nginx.conf`.

---

## Design decisions

- LLMs are used **only for interpretation**, not for signal generation
- Core pipeline stays **deterministic** and reproducible
- Production can use **direct API calls** to a public backend URL to reduce SSL/proxy complexity, or **nginx proxy** in Docker—both patterns are supported via env and build args

---

## Learnings

- Environment differences (local Vite vs Docker vs cloud)
- Keeping API keys out of Git and out of the frontend bundle
- Debugging deployment issues (502, SSL, proxy routing)
- Combining rule-based logic with LLM commentary safely

---

## Future improvements

- Authentication
- Real-time data ingestion
- ML-based predictive models
- Caching and performance tuning
- Multi-asset support

---

## Author

Rahul Khanna
