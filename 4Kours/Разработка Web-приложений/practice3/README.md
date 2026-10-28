# Practice 03 - Fitness Club PostgreSQL

Practice 03 for variant 7: Fitness Club. PostgreSQL stores fitness-club clients
and trainers; Python uses `psycopg` to execute parameterized SQL queries.

## Project structure

```text
practice3/
├── docker-compose.yml
├── create_tables.sql
├── insert_data.sql
├── main.py
├── requirements.txt
└── README.md
```

## Start PostgreSQL

```bash
docker compose up -d
docker compose ps
```

PostgreSQL is available on `localhost:5433` with these credentials:

```text
Database: practice
User: student
Password: student
```

The SQL scripts run automatically only when the named Docker volume is created
for the first time.

## Install Python dependency

```bash
python3 -m pip install -r requirements.txt
```

## Run database operations

```bash
python3 main.py list
python3 main.py get 1
python3 main.py add --name "Olga Smirnova" --membership Premium --trainer-id 1
python3 main.py delete 6
python3 main.py demo
```

`demo` displays all clients, finds a client by ID, creates a temporary client,
deletes that same client, and displays the final table contents.

## Reset the database

```bash
docker compose down -v
docker compose up -d
```

This deletes the PostgreSQL volume and re-runs `create_tables.sql` and
`insert_data.sql`. Do not run this command if you need to keep data created
during the demonstration.

## Parameterized SQL

Every query that contains user input uses `%s` placeholders and passes the
values as a separate tuple, for example:

```python
cursor.execute("DELETE FROM clients WHERE id = %s RETURNING id", (client_id,))
```

This prevents SQL injection and is required by the assignment.
