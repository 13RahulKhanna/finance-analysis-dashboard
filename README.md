📊 Finance Analysis Dashboard

A full-stack financial data pipeline and analysis dashboard that processes market data, generates trading signals, and provides LLM-based insights through an interactive UI.

🚀 Live Demo

👉 https://finance-frontend-pq0l.onrender.com

🧠 Overview

This project implements an end-to-end system that:

Processes OHLCV financial data
Generates trading signals using deterministic logic
Computes key metrics (trend, volatility, signal distribution)
Uses LLMs to interpret results (Groq + OpenRouter)
Displays insights through a modern React dashboard
Includes Docker-based deployment for reproducibility
⚙️ Tech Stack
Backend
Python
FastAPI
Pandas / NumPy
LangChain (LCEL)
Groq API
OpenRouter API
Frontend
React (Vite)
Axios
Recharts (data visualization)
DevOps / Infra
Docker & Docker Compose
Nginx (frontend serving)
Render (deployment)
🔄 System Architecture
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
📈 Features
📊 Financial metrics (trend, volatility, signal rate)
🤖 Dual LLM analysis (Groq vs OpenRouter)
⚠️ Risk & confidence classification
📉 Interactive price trend chart
🔁 End-to-end pipeline execution via API
🌐 Fully deployed system
🧪 API Endpoint
GET /run
Response
{
  "metrics": { ... },
  "groq_analysis": { ... },
  "openrouter_analysis": { ... },
  "chart_data": [ ... ]
}
🛠️ Local Setup
1. Clone repo
git clone https://github.com/13RahulKhanna/finance-analysis-dashboard.git
cd finance-analysis-dashboard
2. Backend setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env:

GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key

Run:

python main.py
3. Frontend setup
cd frontend
npm install
npm run dev
🐳 Docker Setup
docker compose up --build
Frontend → http://localhost:3000
Backend → http://localhost:8000/run
🌐 Deployment
Backend deployed via Docker on Render
Frontend deployed via Docker (Nginx + static build)
API connected directly via public backend endpoint
⚠️ Key Design Decisions
LLM is used only for interpretation, not signal generation
Deterministic pipeline ensures reproducibility
Switched from nginx proxy → direct API calls in production
avoids SSL/proxy issues
simplifies architecture
🧠 Learnings
Differences between local, Docker, and production environments
Handling API keys securely (no secrets in Git)
Debugging real-world deployment issues (502, SSL handshake, proxy routing)
Designing systems where ML/LLM complements logic, not replaces it
📌 Future Improvements
Authentication layer
Real-time data ingestion
Model-based prediction instead of rule-based signals
Caching & performance optimization
Multi-asset support
👨‍💻 Author

Rahul Khanna