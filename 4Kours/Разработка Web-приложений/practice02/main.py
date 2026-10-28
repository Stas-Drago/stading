import os

import psycopg
from fastapi import FastAPI, HTTPException, status
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://student:student@localhost:5433/practice"
)

app = FastAPI(
    title="Fitness Club REST API",
    description="Practice 02 REST API connected to PostgreSQL from Practice 03.",
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


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_client_or_404(client_id: int) -> dict:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, membership, trainer_id FROM clients WHERE id = %s",
            (client_id,),
        )
        client = cursor.fetchone()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def get_trainer_or_404(trainer_id: int) -> dict:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, specialization FROM trainers WHERE id = %s",
            (trainer_id,),
        )
        trainer = cursor.fetchone()

    if trainer is None:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer


@app.get("/info")
def info():
    return {
        "project": "Fitness Club REST API",
        "version": "1.0",
        "variant": 7,
        "entities": ["Client", "Trainer"],
        "storage": "PostgreSQL",
    }


@app.get("/clients", response_model=list[Client])
def get_clients():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT id, name, membership, trainer_id FROM clients ORDER BY id")
        return cursor.fetchall()


@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: int):
    return get_client_or_404(client_id)


@app.post("/clients", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate):
    get_trainer_or_404(client.trainer_id)
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO clients (name, membership, trainer_id)
            VALUES (%s, %s, %s)
            RETURNING id, name, membership, trainer_id
            """,
            (client.name, client.membership, client.trainer_id),
        )
        new_client = cursor.fetchone()
        connection.commit()
    return new_client


@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM clients WHERE id = %s RETURNING id", (client_id,))
        deleted_client = cursor.fetchone()
        connection.commit()

    if deleted_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully", "id": client_id}


@app.get("/trainers", response_model=list[Trainer])
def get_trainers():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT id, name, specialization FROM trainers ORDER BY id")
        return cursor.fetchall()


@app.get("/trainers/{trainer_id}", response_model=Trainer)
def get_trainer(trainer_id: int):
    return get_trainer_or_404(trainer_id)


@app.post("/trainers", response_model=Trainer, status_code=status.HTTP_201_CREATED)
def create_trainer(trainer: TrainerCreate):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO trainers (name, specialization)
            VALUES (%s, %s)
            RETURNING id, name, specialization
            """,
            (trainer.name, trainer.specialization),
        )
        new_trainer = cursor.fetchone()
        connection.commit()
    return new_trainer


@app.delete("/trainers/{trainer_id}")
def delete_trainer(trainer_id: int):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM clients WHERE trainer_id = %s", (trainer_id,))
        has_clients = cursor.fetchone() is not None
        if has_clients:
            raise HTTPException(
                status_code=409,
                detail="Trainer cannot be deleted while clients are assigned",
            )

        cursor.execute("DELETE FROM trainers WHERE id = %s RETURNING id", (trainer_id,))
        deleted_trainer = cursor.fetchone()
        connection.commit()

    if deleted_trainer is None:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return {"message": "Trainer deleted successfully", "id": trainer_id}
