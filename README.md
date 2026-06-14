# URL Shortener

A production-ready URL shortener built with Flask, PostgreSQL, and Nginx — fully containerized with Docker.

This project is built for learning and practicing Docker concepts including multi-stage builds, environment variables, resource limits, custom networking, and reverse proxy configuration.

---

## What It Does

Submit a long URL, get back a short code. Visit the short code and get redirected to the original URL.

**Example:**
```
POST /shorten  {"url": "https://www.google.com"}
→ {"short_code": "2Kdse0"}

GET /2Kdse0
→ redirects to https://www.google.com
```

---

## Architecture

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

All three services run in separate Docker containers on the same internal network. Only Nginx is exposed to the outside world.

---

## Tech Stack

| Service    | Technology      | Purpose                          |
|------------|-----------------|----------------------------------|
| Web        | Flask (Python)  | API — create and redirect URLs   |
| Database   | PostgreSQL 15   | Store short code mappings        |
| Proxy      | Nginx           | Reverse proxy, only public entry |

---

## Project Structure

```
url-shortener/
├── app.py                  ← Flask application
├── requirements.txt        ← Python dependencies
├── Dockerfile              ← Multi-stage build for Flask
├── Dockerfile.nginx        ← Custom Nginx image
├── nginx.conf              ← Nginx reverse proxy config
├── docker-compose.yml      ← All services, limits, volumes
├── .env                    ← Secrets (never pushed to GitHub)
├── .env.example            ← Template for teammates
└── .gitignore              ← Ignores .env
```

---

## Docker Concepts Used

- **Multi-stage build** — builder stage installs packages, final stage runs the app. No pip in production image.
- **Environment variables** — all secrets in `.env`, never hardcoded
- **Resource limits** — CPU and memory limits on all services
- **Custom networking** — Compose creates an internal network, services communicate by name
- **Named volume** — PostgreSQL data persists across restarts
- **Reverse proxy** — Nginx forwards requests to Flask, Flask never directly exposed

---

## Getting Started

### Prerequisites

- Docker Desktop installed and running
- Git

### 1. Clone the repository

```bash
git clone https://github.com/gunjanxy/url-shortner.git
cd url-shortner
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
DB_HOST=db
DB_NAME=urls
DB_USER=your_username
DB_PASSWORD=your_password
POSTGRES_DB=urls
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

### 3. Build and run

```bash
docker compose up --build
```

### 4. Verify all containers are running

```bash
docker ps
```

You should see three containers: `nginx`, `web`, `db`.

---

## Testing the App

### Create a short URL

```bash
# PowerShell
Invoke-WebRequest -Uri http://localhost:8080/shorten -Method POST -ContentType "application/json" -Body '{"url": "https://www.google.com"}'

# Linux / Mac
curl -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Response:**
```json
{"short_code": "2Kdse0"}
```

### Use the short URL

Open in browser:
```
http://localhost:8080/2Kdse0
```

You will be redirected to the original URL.

### Health check

```
http://localhost:8080/health
```

**Response:**
```json
{"status": "healthy"}
```

---

## Environment Variables

| Variable            | Used By    | Description                        |
|---------------------|------------|------------------------------------|
| `DB_HOST`           | Flask      | Database hostname (service name)   |
| `DB_NAME`           | Flask      | Database name                      |
| `DB_USER`           | Flask      | Database username                  |
| `DB_PASSWORD`       | Flask      | Database password                  |
| `POSTGRES_DB`       | PostgreSQL | Database to create on first run    |
| `POSTGRES_USER`     | PostgreSQL | User to create on first run        |
| `POSTGRES_PASSWORD` | PostgreSQL | Password to set on first run       |

> **Note:** `DB_*` and `POSTGRES_*` have the same values but are consumed by different services. Flask reads `DB_*` to connect. PostgreSQL reads `POSTGRES_*` to set itself up.

---

## Resource Limits

| Service | CPU Limit | Memory Limit | CPU Reserved | Memory Reserved |
|---------|-----------|--------------|--------------|-----------------|
| nginx   | 0.5       | 32MB         | 0.25         | 16MB            |
| web     | 0.5       | 128MB        | 0.25         | 64MB            |
| db      | 1.0       | 512MB        | 0.5          | 256MB           |

---

## Docker Hub

Images are available on Docker Hub:

- `gunjanjain24/url-shortener-web:v1`
- `gunjanjain24/url-shortener-nginx:v1`

```bash
docker pull gunjanjain24/url-shortener-web:v1
docker pull gunjanjain24/url-shortener-nginx:v1
```

---

## Stopping the App

```bash
docker compose down
```

To also delete the database volume:

```bash
docker compose down -v
```

---

## Author

Gunjan Jain
Learning Docker, DevOps, and Cloud Infrastructure.
