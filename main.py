from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from starlette import status

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskCreate(BaseModel):
    name: str
    description: str

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post("/tasks/", response_model=TaskResponse)
async def create_item(item: TaskCreate, db: Session = Depends(get_db)):
    db_item = Task(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/tasks/", response_model=List[TaskResponse])
async def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Task).filter(Task.id == task_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_item)
    db.commit()
    return

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def read_item(task_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Task).filter(Task.id == task_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_item
# Getting tasks by id is unused for now, but was in a tutorial, so for now it can stay

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="mainpage.html"
    )