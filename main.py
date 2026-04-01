# https://github.com/EPF-MDE/fastapi-coffee-experiment/blob/master/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date

"""
to do :
add a database for users and prohect
html pages
"""

app = FastAPI()


class Project(BaseModel):
    name: str
    date_start: date
    date_end: date | None = None
    image_path: str | None = None
    description: str
    link: str | None = None
    dotlist: list[str] | None = None


class User(BaseModel):
    name: str
    firstname: str
    age: int
    email: str
    github: str | None = None
    tel: str | None = None
    projects: list[Project]


users: list[User] = [
    User(
        name="Letort",
        firstname="Adrien",
        age=22,
        email="adrien.letort@epfedu.frf",
        tel="06 12 13 14 15",
        projects=[
            Project(
                name="RenovTaCana",
                date_start=date(2026, 4, 1),
                image_path="string",
                description="Projet de semestre 4a epf",
            )
        ],
    )
]


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <h1> Home Page !</h1>
    <p>users list : {users} </p>
    """


@app.get("/users")
def get_all_users():
    return [
        f"ID: {index}, name: {user.name} {user.firstname}\n"
        for index, user in enumerate(users)
    ]


@app.post("/add_user")
def add_user(user: User):
    users.append(user)
    return {"user_id": len(users) - 1}


@app.post("/add_project/{user_id}")
def add_project(user_id: int, project: Project):
    users[user_id].projects.append(project)
    return {"user": users[user_id]}


@app.post("/remove_project")
def remove_project(user_id: int, project_id: int):
    users[user_id].projects.pop(project_id)
    return {
        "message": f"removed project {project_id} from {users[user_id].firstname} {users[user_id].name}"
    }


@app.post("/remove_user/{user_id}")
def remove_user(user_id: int):
    users.pop(user_id)
    return {"message": f"removed user {user_id}"}
