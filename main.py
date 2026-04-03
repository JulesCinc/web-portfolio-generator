# https://github.com/EPF-MDE/fastapi-coffee-experiment/blob/master/main.py
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from datetime import date
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

"""
to do :
add a database for users and prohect    
html pages
"""


class Project(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True)
    user_id: int
    name: str
    date_start: date
    date_end: date | None = None
    image_path: str | None = None
    description: str
    link: str | None = None
    dotlist: str | None = None


class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    name: str
    firstname: str
    age: int
    email: str
    github: str | None = None
    tel: str | None = None


# Create engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create DB
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1> Home Page !</h1>
    """


@app.post("/add_user")
def add_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.post("/add_project")
def add_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/users")
def get_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users


@app.get("/get_user/{user_id}")
def get_user_by_id(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @app.post("/remove_project")
# def remove_project(user_id: int, project_id: int):
#     users[user_id].projects.pop(project_id)
#     return {
#         "message": f"removed project {project_id} from {users[user_id].firstname} {users[user_id].name}"
#     }


@app.delete("/remove_user/{user_id}")
def delete_user_by_id(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"response": f"removed user {user_id}"}
