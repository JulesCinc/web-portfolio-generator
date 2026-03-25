# https://github.com/EPF-MDE/fastapi-coffee-experiment/blob/master/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = []


class Project(BaseModel):
    name: str
    description: str


class User(BaseModel):
    name: str
    age: int
    email: str
    tel: str
    projects: list[Project] | None = None


@app.get("/")
def home():
    return "Welcom on the web portfolio geneator"


@app.post("/add_user")
def add_user(user: User):
    users.append(user)
    return {"user_id": len(users) - 1}


@app.post("/add_project/{user_id}")
def add_project(user_id: int, project: Project):
    return {"project": project}


@app.get("/users")
def get_all_users():
    return users


@app.get("/remove_user")
def remove_user(user: User):
    return {"message": "pas finie"}
