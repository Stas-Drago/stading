import argparse
import os

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://student:student@localhost:5433/practice"
)


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_all_clients(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT clients.id, clients.name, clients.membership, trainers.name AS trainer
            FROM clients
            JOIN trainers ON trainers.id = clients.trainer_id
            ORDER BY clients.id
            """
        )
        return cursor.fetchall()


def get_client_by_id(connection, client_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT clients.id, clients.name, clients.membership, trainers.name AS trainer
            FROM clients
            JOIN trainers ON trainers.id = clients.trainer_id
            WHERE clients.id = %s
            """,
            (client_id,),
        )
        return cursor.fetchone()


def add_client(connection, name, membership, trainer_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO clients (name, membership, trainer_id)
            VALUES (%s, %s, %s)
            RETURNING id, name, membership, trainer_id
            """,
            (name, membership, trainer_id),
        )
        client = cursor.fetchone()
    connection.commit()
    return client


def delete_client(connection, client_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM clients WHERE id = %s RETURNING id", (client_id,))
        deleted_client = cursor.fetchone()
    connection.commit()
    return deleted_client


def print_clients(clients):
    if not clients:
        print("No clients found.")
        return

    for client in clients:
        trainer = client["trainer"] if "trainer" in client else client["trainer_id"]
        print(
            f"ID: {client['id']}; Name: {client['name']}; "
            f"Membership: {client['membership']}; Trainer: {trainer}"
        )


def run_demo(connection):
    print("All clients:")
    print_clients(get_all_clients(connection))

    print("\nClient with ID 1:")
    print(get_client_by_id(connection, 1))

    print("\nAdding a client:")
    new_client = add_client(connection, "Demo Client", "Standard", 1)
    print(new_client)

    print("\nDeleting the created client:")
    print(delete_client(connection, new_client["id"]))

    print("\nClients after deletion:")
    print_clients(get_all_clients(connection))


def parse_arguments():
    parser = argparse.ArgumentParser(description="Fitness Club PostgreSQL client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Show all clients")

    get_parser = subparsers.add_parser("get", help="Find a client by ID")
    get_parser.add_argument("id", type=int)

    add_parser = subparsers.add_parser("add", help="Add a client")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--membership", required=True)
    add_parser.add_argument("--trainer-id", required=True, type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete a client by ID")
    delete_parser.add_argument("id", type=int)

    subparsers.add_parser("demo", help="Run all required database operations")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with get_connection() as connection:
        if args.command == "list":
            print_clients(get_all_clients(connection))
        elif args.command == "get":
            print(get_client_by_id(connection, args.id))
        elif args.command == "add":
            print(add_client(connection, args.name, args.membership, args.trainer_id))
        elif args.command == "delete":
            print(delete_client(connection, args.id))
        elif args.command == "demo":
            run_demo(connection)


if __name__ == "__main__":
    main()
