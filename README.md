# backend-asessment

This project contains two services and a shared Docker Compose setup:

- `mock-server`: a Flask API that serves customer fixture data from JSON
- `pipeline-service`: a FastAPI service that ingests customers from the mock server into Postgres and exposes DB-backed customer endpoints
- `postgres`: the database used by the pipeline service

## Project Structure

```text
.
├── docker-compose.yml
├── mock-server
│   ├── app.py
│   ├── data/customer.json
│   ├── Dockerfile
│   └── requirements.txt
├── pipeline-service
│   ├── database.py
│   ├── main.py
│   ├── models/customer.py
│   ├── services/ingestion.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

## Services

### Mock Server

The mock server exposes customer fixture data through Flask.

Endpoints:

- `GET /api/health`
- `GET /api/customers?page=1&limit=10`
- `GET /api/customers/<customer_id>`

### Pipeline Service

The pipeline service uses FastAPI and SQLAlchemy.

Endpoints:

- `POST /api/ingest`
- `GET /api/customers?page=1&limit=10`
- `GET /api/customers/<customer_id>`

## Data Model

The `customers` table contains:

- `customer_id`
- `first_name`
- `last_name`
- `email`
- `phone`
- `address`
- `date_of_birth`
- `account_balance`
- `created_at`

## Running With Docker

Start everything with:

```bash
docker-compose up -d --build
```

Services run on:

- Mock server: `http://localhost:5000`
- Pipeline service: `http://localhost:8000`

## Useful Requests

Check mock server health:

```bash
curl http://localhost:5000/api/health
```

Fetch mock customers:

```bash
curl "http://localhost:5000/api/customers?page=1&limit=10"
```

Ingest customers into Postgres:

```bash
curl -X POST http://localhost:8000/api/ingest
```

Read customers from the pipeline service:

```bash
curl "http://localhost:8000/api/customers?page=1&limit=10"
```

Fetch one customer from the pipeline service:

```bash
curl http://localhost:8000/api/customers/CUST-1001
```

## Environment

The Compose setup passes:

- `DATABASE_URL=postgresql+psycopg://postgres:password@postgres:5432/customer_db`
- `MOCK_SERVER_URL=http://mock-server:5000`

## Notes

- The pipeline service uses upsert behavior when ingesting customers, so repeated ingests update existing rows instead of failing on primary key conflicts.
- The mock server listens on `0.0.0.0:5000` inside Docker so the published port works correctly.
