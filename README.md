# Finance Analysis Dashboard

A full-stack application for processing time-series market data, generating trading signals, and presenting results through a web-based dashboard.

---

## Overview

This project implements a batch processing pipeline for financial data and exposes the results through an API and a web interface.

The system is designed with clear separation between:

- Data processing (pipeline)
- API layer (FastAPI)
- Presentation layer (React)

---

## Architecture


Frontend (React)
↓
FastAPI (/run)
↓
Pipeline (data processing, signal generation)
↓
LLM layer (optional interpretation)
↓
Structured JSON response


---

## Features

### Data Pipeline
- Processes OHLCV-style time series data
- Computes rolling mean-based signals
- Generates aggregate metrics (trend, volatility, signal counts)
- Configurable via YAML

### API
- FastAPI-based endpoint: `GET /run`
- Returns structured JSON
- No side effects (no file writes during API calls)

### Frontend
- React (Vite)
- Component-based structure
- Displays:
  - Metrics
  - Analysis summaries
  - Model comparison
  - Price trend chart

### Visualization
- Line chart of price over time
- Signal-aware markers
- Backend-driven downsampling for performance

---

## Project Structure


.
├── pipeline/
│ ├── data_processing.py
│ ├── signals.py
│ └── config.yaml
├── llm/
│ └── llm_analysis.py
├── frontend/
│ ├── src/
│ └── package.json
├── main.py
├── requirements.txt
└── Dockerfile


---

## Installation

### Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env:

GROQ_API_KEY=...
OPENROUTER_API_KEY=...

Run:

uvicorn main:app --reload
Frontend
cd frontend
npm install
npm run dev

Open:

http://localhost:5173
API
GET /run

Returns:

{
  "metrics": {...},
  "groq_analysis": {...},
  "openrouter_analysis": {...},
  "chart_data": [...]
}
Design Notes
Signal generation is deterministic and handled entirely in the pipeline
Interpretation is separated from computation
Chart data is generated server-side to avoid duplicating logic in the client
API responses are structured and validated before being returned
Deployment
Backend
Compatible with platforms such as Render, Railway, Fly.io
Requires environment variables for API keys
Frontend
Deployable on Vercel or Netlify
Configure API base URL via environment variables
Performance Considerations
Chart data is downsampled (~400 points) to reduce payload size
No animation or heavy computation in React render cycle
Canvas-based background animation is isolated from React state
Future Work
Support multiple datasets
Add backtesting for signal evaluation
Introduce authentication and persistence
Improve error reporting and observability