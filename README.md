# weather-ai-tracking

A personal project to track weather data for Portuguese cities and ask an AI about it. Built to explore FastAPI, React, PostgreSQL, and Kubernetes — and to actually understand how these pieces fit together in a real stack.

---

## What it does

You add cities, a background worker fetches weather data from OpenWeatherMap on a schedule, and everything gets stored in a database. There's also a small AI chat where you can ask things like "what's the average temperature in Lisbon this week?" and get a straight answer based on the stored data.

---

## Stack

- **Backend** — FastAPI + Python
- **Frontend** — React + Vite
- **Database** — PostgreSQL + SQLAlchemy
- **AI** — Groq or Ollama (switchable via env var)
- **Weather data** — OpenWeatherMap API
- **Infra** — Docker, Kubernetes (Minikube locally, EKS for cloud)

---

## Project structure

```
weather-ai-tracking/
├── api.py                  # API endpoints
├── services.py             # Weather fetching and AI logic
├── models.py               # Database models
├── database.py             # DB connection
├── worker.py               # Fetches weather for all tracked cities
├── llm_integration.py      # Abstract base for LLM providers
├── llm_factory.py          # Picks the right LLM client based on config
├── create_tables.py        # Run once to set up the DB
├── Dockerfile
├── docker-compose.yml
├── adapters/
│   ├── groq_adapter.py
│   └── ollama_adapter.py
├── frontend/
├── k8s/
│   ├── namespace.yaml
│   ├── api-deployment.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-pvc.yaml
│   ├── weather-secret.yaml
│   └── cronjob.yaml
├── scripts/
│   └── deploy.sh
└── tests/
    ├── test_api.py
    └── test_services.py
```

---

## Running locally with Docker Compose

### 1. Create a `.env` file

```env
WEATHER_API_KEY=your_openweathermap_key
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_key
AI_MODEL=llama3-8b-8192
DATABASE_URL=postgresql://admin:admin@localhost:5432/postgres
```

### 2. Start everything

```bash
docker compose up --build
```

### 3. Create the tables (first time only)

```bash
docker compose exec api python create_tables.py
```

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Go to http://localhost:5173.

### Fetch weather manually

```bash
docker compose run --rm worker
```

---

## Running on Kubernetes (Minikube)

This is where the CronJob actually runs — fetching weather 3 times a day automatically.

### First time

```bash
minikube start
eval $(minikube docker-env)
docker build -t weather-app:latest .
kubectl apply -f k8s/
kubectl exec -n weather-app deployment/weather-api -- python create_tables.py
minikube tunnel
```

### After that (no code changes)

```bash
minikube start
minikube tunnel
```

### After changing code

```bash
./scripts/deploy.sh
```

This rebuilds the image inside Minikube and restarts the deployment.

### Auto-deploy on commit

```bash
echo '#!/bin/bash\n./scripts/deploy.sh' > .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/weather` | All weather records |
| GET | `/weather/{city_name}` | Records for a specific city |
| GET | `/cities` | Tracked cities |
| POST | `/cities?name={city}` | Add a city |
| DELETE | `/cities/{city_name}` | Remove a city |
| POST | `/ai/ask?question={question}` | Ask the AI |

Swagger docs at http://localhost:8000/docs.

---

## AI providers

Switch between providers with the `AI_PROVIDER` env var.

**Groq** (needs an API key, fast)
```env
AI_PROVIDER=groq
GROQ_API_KEY=your_key
AI_MODEL=llama3-8b-8192
```

**Ollama** (runs locally, no key needed)
```env
AI_PROVIDER=ollama
AI_MODEL=llama3
```

---

## CronJob

Runs 3 times a day at 8h, 12h and 20h UTC (9h, 13h, 21h in Portugal during summer):

```
0 8,12,20 * * *
```

---

## Checking the database

### Via psql

```bash
kubectl exec -it -n weather-app deployment/postgres -- psql -U admin -d postgres
```

### Via DBeaver

Forward the port first:

```bash
kubectl port-forward -n weather-app deployment/postgres 5432:5432
```

Then connect with `localhost:5432`, user `admin`, password `admin`.

---

## Tests

```bash
pytest tests/
```
