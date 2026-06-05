# https://github.com/EPF-MDE/fastapi-coffee-experiment/blob/master/main.py
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Project(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True)
    user_id: int
    name: str
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

templates = Jinja2Templates(directory="template")


# Create DB
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/userspage")
def see_users_page(request: Request, session: SessionDep):
    users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"users": users},
    )


@app.get("/add-user-page")
def add_user_page(request: Request):
    return templates.TemplateResponse(request, "add-user.html")


@app.get("/cv/{user_id}")
def cv_page(request: Request, user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = session.exec(select(Project).where(Project.user_id == user_id)).all()

    return templates.TemplateResponse(
        request=request,
        name="cv.html",
        context={"user": user, "projects": projects},
    )


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


@app.get("/get_user/{user_id}/projects")
def get_user_projects(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = session.exec(select(Project).where(Project.user_id == user_id)).all()

    return projects


@app.delete("/remove_project/{project_id}")
def delete_project_by_id(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"response": f"removed project {project_id}"}


@app.delete("/remove_user/{user_id}")
def delete_user_by_id(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete projects
    projects = session.exec(select(Project).where(Project.user_id == user_id)).all()
    for project in projects:
        session.delete(project)

    # Delete user
    session.delete(user)

    session.commit()
    return {"response": f"removed user {user_id} and associated project(s)"}
