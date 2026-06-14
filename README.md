# URL Shortener — Docker Project
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Docker Hub](https://img.shields.io/badge/Docker%20Hub-gunjanjain24-2496ED?style=for-the-badge&logo=docker&logoColor=white)
A production-ready URL shortener built with Flask, PostgreSQL, and Nginx — fully containerized with Docker.

This repository is created for learning and practicing Docker concepts including multi-stage builds, environment variables, resource limits, custom networking, and reverse proxy configuration.

---

# Project Goals

The main goal of this project is to practice:

- Docker multi-stage builds
- Environment variable management with `.env` files
- Container resource limits (CPU and memory)
- Docker networking and service discovery
- Nginx as a reverse proxy
- Docker Compose for multi-container applications
- Pushing images to Docker Hub

This is a learning project built while studying Docker and DevOps concepts.

---

# What It Does

Submit a long URL and get back a short code. Visit the short code and get redirected to the original URL.

**Example:**
```
POST /shorten  {"url": "https://www.google.com"}
→ {"short_code": "2Kdse0"}

GET /2Kdse0
→ redirects to https://www.google.com
```

---

# Architecture

```
Browser / Client
      │
      ▼
 Nginx (port 8080)          ← only service exposed to internet
      │
      ▼
 Flask / Web (port 5000)    ← handles application logic
      │
      ▼
 PostgreSQL (port 5432)     ← stores short code → URL mappings
```

All three services run in separate Docker containers on the same internal network. Only Nginx is exposed to the outside world. Flask and PostgreSQL are never directly accessible.

---

# Current Features

## URL Management

- Create short codes from long URLs via POST request
- Redirect short codes to original URLs via GET request
- Health check endpoint

## Docker Features

- Multi-stage Dockerfile — builder installs packages, final stage runs app. No pip in production image.
- Environment variables via `.env` file — secrets never hardcoded
- Resource limits — CPU and memory limits on all services
- Named volume — PostgreSQL data persists across container restarts
- Custom networking — services communicate by name via Docker DNS

## Security

- Nginx reverse proxy — Flask never directly exposed
- `.env` excluded from version control via `.gitignore`
- No pip or build tools in production image — reduced attack surface

---

# Technologies Used

- Python / Flask
- PostgreSQL 15
- Nginx
- Docker & Docker Compose
- psycopg2-binary
- Git & GitHub
- Docker Hub

---

# Project Structure

```
url-shortener/
│
├── app.py                  ← Flask application
├── requirements.txt        ← Python dependencies
├── Dockerfile              ← Multi-stage build for Flask
├── Dockerfile.nginx        ← Custom Nginx image
├── nginx.conf              ← Nginx reverse proxy configuration
├── docker-compose.yml      ← All services, limits, volumes
├── .env                    ← Secrets (never pushed to GitHub)
├── .env.example            ← Template for teammates
└── .gitignore              ← Ignores .env
```

---

# Environment Variables

| Variable            | Used By    | Description                        |
|---------------------|------------|------------------------------------|
| `DB_HOST`           | Flask      | Database hostname (service name)   |
| `DB_NAME`           | Flask      | Database name                      |
| `DB_USER`           | Flask      | Database username                  |
| `DB_PASSWORD`       | Flask      | Database password                  |
| `POSTGRES_DB`       | PostgreSQL | Database to create on first run    |
| `POSTGRES_USER`     | PostgreSQL | User to create on first run        |
| `POSTGRES_PASSWORD` | PostgreSQL | Password to set on first run       |

> `DB_*` and `POSTGRES_*` have the same values but are read by different services. Flask reads `DB_*` to connect. PostgreSQL reads `POSTGRES_*` to set itself up on first startup.

---

# Resource Limits

| Service | CPU Limit | Memory Limit | CPU Reserved | Memory Reserved |
|---------|-----------|--------------|--------------|-----------------|
| nginx   | 0.5       | 32MB         | 0.25         | 16MB            |
| web     | 0.5       | 128MB        | 0.25         | 64MB            |
| db      | 1.0       | 512MB        | 0.5          | 256MB           |

---

# How to Run

## Prerequisites

- Docker Desktop installed and running
- Git

## 1. Clone the repository

```bash
git clone https://github.com/gunjanxy/url-shortner.git
cd url-shortner
```

## 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
DB_HOST=db
DB_NAME=your_db_name
DB_USER=your_username
DB_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

## 3. Build and run

```bash
docker compose up --build
```

## 4. Verify containers are running

```bash
docker ps
```

You should see three containers: `nginx`, `web`, `db`.

---

# Testing the App

## Create a short URL

```bash
# PowerShell
Invoke-WebRequest -Uri http://localhost:8080/shorten -Method POST -ContentType "application/json" -Body '{"url": "https://www.google.com"}'

# Linux / Mac
curl -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

Response:
```json
{"short_code": "2Kdse0"}
```

## Use the short URL

Open in browser:
```
http://localhost:8080/2Kdse0
```

You will be redirected to the original URL.

## Health check

```
http://localhost:8080/health
```

Response:
```json
{"status": "healthy"}
```

---

# Stopping the App

```bash
docker compose down
```

To also delete the database volume:

```bash
docker compose down -v
```

---

# Docker Hub

Images are available on Docker Hub:

```bash
docker pull gunjanjain24/url-shortener-web:v1
docker pull gunjanjain24/url-shortener-nginx:v1
```

---

# Important Notes

- This project is created for learning and practice purposes
- Never push `.env` to GitHub — it contains real credentials
- Always use `.env.example` to share environment variable structure with teammates
- Resource limits should be adjusted based on actual `docker stats` measurements in production

---

# Learning Focus

This project helped practice concepts such as:

- Docker multi-stage builds and image optimization
- Environment variable management and secrets handling
- Container resource limits and monitoring
- Docker networking and embedded DNS
- Nginx reverse proxy configuration
- Docker Compose multi-service orchestration
- Docker Hub image publishing

---

# Author

Gunjan Jain

Learning Docker, DevOps, and Cloud Infrastructure.
