from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Fitness Club REST API",
    description="Practice 02. Variant 7: Fitness Club.",
    version="1.0.0",
)


class TrainerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    specialization: str = Field(min_length=2, max_length=100)


class Trainer(TrainerCreate):
    id: int


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    membership: str = Field(min_length=2, max_length=50)
    trainer_id: int = Field(gt=0)


class Client(ClientCreate):
    id: int


trainers = [
    {"id": 1, "name": "Elena Smirnova", "specialization": "Strength training"},
    {"id": 2, "name": "Dmitry Volkov", "specialization": "Fitness and cardio"},
]

clients = [
    {"id": 1, "name": "Alex Ivanov", "membership": "Premium", "trainer_id": 1},
    {"id": 2, "name": "Maria Petrova", "membership": "Standard", "trainer_id": 2},
]


def get_record(records: list[dict], record_id: int, detail: str) -> dict:
    for record in records:
        if record["id"] == record_id:
            return record
    raise HTTPException(status_code=404, detail=detail)


def next_id(records: list[dict]) -> int:
    return max((record["id"] for record in records), default=0) + 1


@app.get("/info")
async def info():
    return {
        "project": "Fitness Club REST API",
        "version": "1.0",
        "variant": 7,
        "entities": ["Client", "Trainer"],
    }


@app.get("/clients", response_model=list[Client])
async def get_clients():
    return clients


@app.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: int):
    return get_record(clients, client_id, "Client not found")


@app.post("/clients", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate):
    get_record(trainers, client.trainer_id, "Trainer not found")
    new_client = {"id": next_id(clients), **client.model_dump()}
    clients.append(new_client)
    return new_client


@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    client = get_record(clients, client_id, "Client not found")
    clients.remove(client)
    return {"message": "Client deleted successfully", "id": client_id}


@app.get("/trainers", response_model=list[Trainer])
async def get_trainers():
    return trainers


@app.get("/trainers/{trainer_id}", response_model=Trainer)
async def get_trainer(trainer_id: int):
    return get_record(trainers, trainer_id, "Trainer not found")


@app.post("/trainers", response_model=Trainer, status_code=status.HTTP_201_CREATED)
async def create_trainer(trainer: TrainerCreate):
    new_trainer = {"id": next_id(trainers), **trainer.model_dump()}
    trainers.append(new_trainer)
    return new_trainer


@app.delete("/trainers/{trainer_id}")
async def delete_trainer(trainer_id: int):
    trainer = get_record(trainers, trainer_id, "Trainer not found")
    if any(client["trainer_id"] == trainer_id for client in clients):
        raise HTTPException(
            status_code=409,
            detail="Trainer cannot be deleted while clients are assigned",
        )
    trainers.remove(trainer)
    return {"message": "Trainer deleted successfully", "id": trainer_id}
