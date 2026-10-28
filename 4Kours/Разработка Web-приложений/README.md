# Practice 01 - Fitness Club API

FastAPI backend for laboratory work.

## Variant

- Variant: 7
- Theme: Fitness Club
- Entities: Client, Trainer

## Run

```bash
python3 -m uvicorn main:app --reload
```

When port `8000` is occupied by another project, run the laboratory work on port
`8001`:

```bash
python3 -m uvicorn main:app --reload --port 8001
```

## Docker

Build and run the application in Docker:

```bash
docker compose up --build
```

The API will be available at <http://127.0.0.1:8001> and Swagger UI at
<http://127.0.0.1:8001/docs>. Stop the container with `docker compose down`.

## URLs

- <http://127.0.0.1:8001>
- <http://127.0.0.1:8001/docs>

## Endpoints

- `GET /`
- `GET /about`
- `GET /users`
- `GET /info`
- `GET /hello`
- `GET /contacts`
- `GET /status`
- `GET /clients`
- `GET /clients/{client_id}`
- `GET /trainers`
- `GET /trainers/{trainer_id}`
