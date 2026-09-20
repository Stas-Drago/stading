# Practice 01 - University API

FastAPI backend for laboratory work.

## Variant

- Variant: 4
- Theme: University
- Entities: Student, Group

## Run

```bash
python3 -m uvicorn main:app --reload
```

## URLs

- <http://127.0.0.1:8000>
- <http://127.0.0.1:8000/docs>

## Endpoints

- `GET /`
- `GET /about`
- `GET /users`
- `GET /info`
- `GET /students`
- `GET /students/{student_id}`
- `GET /groups`
- `GET /groups/{group_id}`
