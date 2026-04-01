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

users = []


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
    age: int
    email: str
    github: str | None = None
    tel: str | None = None
    projects: list[Project]


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <h1> Home Page !</h1>
    <p>users list : {users} </p>
    """


@app.get("/users")
def get_all_users():
    return [f"ID: {index}, name: {user.name}" for index, user in enumerate(users)]


@app.post("/add_user")
def add_user(user: User):
    users.append(user)
    return {"user_id": len(users) - 1}


@app.post("/add_project/{user_id}")
def add_project(user_id: int, project: Project):
    users[user_id].projects.append(project)
    return {"user": users[user_id]}


@app.get("/remove_project/{project_id}")
def remove_project(project_id):
    # todo
    return {"test": "test"}


@app.get("/remove_user")
def remove_user(user: User):
    # todo
    return {"message": "pas finie"}
