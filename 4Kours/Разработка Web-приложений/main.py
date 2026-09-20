from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="University API",
    description="Practice 01 FastAPI backend. Variant 4: University.",
    version="1.0.0",
)

students = [
    {
        "id": 1,
        "first_name": "Alex",
        "last_name": "Ivanov",
        "group_id": 1,
        "email": "alex.ivanov@university.example",
    },
    {
        "id": 2,
        "first_name": "Maria",
        "last_name": "Petrova",
        "group_id": 1,
        "email": "maria.petrova@university.example",
    },
    {
        "id": 3,
        "first_name": "Ivan",
        "last_name": "Sidorov",
        "group_id": 2,
        "email": "ivan.sidorov@university.example",
    },
]

groups = [
    {
        "id": 1,
        "name": "WEB-41",
        "course": 4,
        "speciality": "Web Development",
    },
    {
        "id": 2,
        "name": "SE-42",
        "course": 4,
        "speciality": "Software Engineering",
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
        "variant": 4,
        "theme": "University",
        "entities": ["Student", "Group"],
    }


@app.get("/students")
async def get_students():
    return {"students": students}


@app.get("/students/{student_id}")
async def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/groups")
async def get_groups():
    return {"groups": groups}


@app.get("/groups/{group_id}")
async def get_group(group_id: int):
    for group in groups:
        if group["id"] == group_id:
            group_students = [
                student for student in students if student["group_id"] == group_id
            ]
            return {**group, "students": group_students}

    raise HTTPException(status_code=404, detail="Group not found")
