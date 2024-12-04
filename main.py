from typing import Annotated, Union
from fastapi import Depends, FastAPI, Query, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
import requests
from faker import Faker

fake = Faker()

class Person():
  def __init__(self, id: int, name: str, job: str, company: str, location: str, dob: str, favorite_color: str):
    self.id = id
    self.name = name
    self.job = job
    self.company = company
    self.location = location
    self.dob = dob
    self.favorite_color = favorite_color
      
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def home_view(request: Request):
    todos = get_todos_from_external_api()

    people = []
    for i in range(200):
        person = Person(
            id=i,
            name=fake.name(),
            job=fake.job(),
            company=fake.company(),
            location=fake.country(),
            dob=fake.date_of_birth(),
            favorite_color=fake.color_name()
        )
        people.append(person)
    
    return templates.TemplateResponse("index.html", {"request": request, "something_here": "I can add string this to template", "people": people, "todos":todos })


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


class Todo:
    id: int
    user_id: int
    title: str
    completed: bool

def get_todos_from_external_api() -> list[Todo]:
    todos = []
    """Fetches todos from external API and maps the response to our Todo objects."""
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    todos_data = response.json()
    return todos_data
