# Practice 02 - Fitness Club REST API

REST API for Practice 02, variant 7: Fitness Club.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8002
```

Open the API at <http://127.0.0.1:8002> and Swagger UI at
<http://127.0.0.1:8002/docs>.

Port `8002` keeps this work separate from DentalHelper (`8000`) and Practice 01
(`8001`).

## Endpoints

| Method | URL | Description | Expected status |
| --- | --- | --- | --- |
| GET | `/info` | Project information | 200 |
| GET | `/clients` | All clients | 200 |
| GET | `/clients/{client_id}` | Client by ID | 200 or 404 |
| POST | `/clients` | Create a client | 201 or 404 |
| DELETE | `/clients/{client_id}` | Delete a client | 200 or 404 |
| GET | `/trainers` | All trainers | 200 |
| GET | `/trainers/{trainer_id}` | Trainer by ID | 200 or 404 |
| POST | `/trainers` | Create a trainer | 201 |
| DELETE | `/trainers/{trainer_id}` | Delete a trainer | 200, 404, or 409 |

## Example JSON for POST /clients

```json
{
  "name": "Olga Smirnova",
  "membership": "Premium",
  "trainer_id": 1
}
```

## DevTools check

Open Swagger UI, execute one `GET /clients` request and one `POST /clients`
request. In the browser press `F12`, open **Network**, select each request, and
inspect **Headers** and **Response**. Record the HTTP method, request URL,
status code, request headers, response headers, and response body.
