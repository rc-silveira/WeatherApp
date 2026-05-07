# weather-ai-tracking

A personal project to track weather data and ask an AI about it. Built to get hands-on with FastAPI, React, PostgreSQL, and Kubernetes. Not just each piece in isolation, but the whole stack working together.

You add cities, a background worker fetches weather from OpenWeatherMap on a schedule, and everything lands in a database. There's also a small AI chat where you can ask things like "what's the average temperature in Lisbon this week?" and get an actual answer based on the stored data.

---

## Stack

- **Backend** — FastAPI + Python
- **Frontend** — React + Vite
- **Database** — PostgreSQL + SQLAlchemy
- **AI** — Groq (preferred) or Ollama
- **Weather data** — OpenWeatherMap API
- **Infra** — Docker, Kubernetes (Minikube locally, EKS for cloud)

---

## Project structure

The core is all in the root — `api.py`, `services.py`, `models.py`, `worker.py`. The `adapters/` folder has the clients for Groq and Ollama, and `llm_factory.py` picks which one to use based on the env. The rest is what it looks like: `frontend/`, `k8s/`, `scripts/`, `tests/`.

---

## Running locally with Docker Compose

### 1. Create a `.env` file

```env
WEATHER_API_KEY=openweathermap_key
AI_PROVIDER=groq
GROQ_API_KEY=groq_key
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

This is where the CronJob runs — fetching weather 3 times a day automatically.

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

Rebuilds the image inside Minikube and restarts the deployment.

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

Groq is faster and more reliable in practice. Ollama is there if you want to run everything locally.

**Groq**
```env
AI_PROVIDER=groq
GROQ_API_KEY=key
AI_MODEL=llama3-8b-8192
```

**Ollama**
```env
AI_PROVIDER=ollama
AI_MODEL=llama3
```

---

## CronJob

Runs 3 times a day at 8h, 12h and 20h UTC — 9h, 13h, 21h in Portugal during summer.

```
0 8,12,20 * * *
```

---

## Checking the database

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