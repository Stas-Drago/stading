from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Fitness Club API",
    description="Practice 01 FastAPI backend. Variant 7: Fitness Club.",
    version="1.0.0",
)

clients = [
    {
        "id": 1,
        "name": "Alex Ivanov",
        "membership": "Premium",
        "trainer_id": 1,
    },
    {
        "id": 2,
        "name": "Maria Petrova",
        "membership": "Standard",
        "trainer_id": 2,
    },
    {
        "id": 3,
        "name": "Ivan Sidorov",
        "membership": "Premium",
        "trainer_id": 1,
    },
]

trainers = [
    {
        "id": 1,
        "name": "Elena Smirnova",
        "specialization": "Strength training",
    },
    {
        "id": 2,
        "name": "Dmitry Volkov",
        "specialization": "Fitness and cardio",
    },
]


@app.get("/")
async def root():
    return {"message": "Hello Web"}


@app.get("/about")
async def about():
    return {"course": "Web Development"}


@app.get("/users")
async def users():
    return {"users": ["Alex", "Maria", "Ivan"]}


@app.get("/info")
async def info():
    return {
        "variant": 7,
        "theme": "Fitness Club",
        "entities": ["Client", "Trainer"],
    }


@app.get("/hello")
async def hello():
    return {"message": "Welcome to Fitness Club"}


@app.get("/contacts")
async def contacts():
    return {"phone": "+7-999-123-45-67", "email": "info@fitness-club.example"}



@app.get("/status")
async def status():
    return {"status": "open", "message": "Fitness Club is working"}


@app.get("/clients")
async def get_clients():
    return {"clients": clients}


@app.get("/clients/{client_id}")
async def get_client(client_id: int):
    for client in clients:
        if client["id"] == client_id:
            return client

    raise HTTPException(status_code=404, detail="Client not found")


@app.get("/trainers")
async def get_trainers():
    return {"trainers": trainers}


@app.get("/trainers/{trainer_id}")
async def get_trainer(trainer_id: int):
    for trainer in trainers:
        if trainer["id"] == trainer_id:
            trainer_clients = [
                client for client in clients if client["trainer_id"] == trainer_id
            ]
            return {**trainer, "clients": trainer_clients}

    raise HTTPException(status_code=404, detail="Trainer not found")
