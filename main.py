from fastapi import FastAPI, HTTPException, Request, status, Form
import models
from database import engine
from sqlalchemy.orm import Session
import sqlite3
from models import Project, Team
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


models.meta_data_obj.create_all(engine)
models.meta_data_obj1.create_all(engine)
models.meta_data_obj2.create_all(engine)

app = FastAPI()

conn = sqlite3.connect('sqlbase.db', check_same_thread=False)
cursor = conn.cursor()

def delete_all():
    cursor.execute("DELETE FROM team")
    cursor.execute("DELETE FROM project")
    cursor.execute("DELETE FROM team_and_project")
    conn.commit()


@app.get("/")
def root():
    return {"message": "Hello!"}


@app.get("/status")
def get_status():
    try:
        conn
        return 'Service is ready to receive requests.'
    except HTTPException:
        return "Service is stopped."


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.put("/teams")
def put_teams(team: List[Team]):
    length = len(team)
    delete_all()
    for i in range(length):
        team_id = team[i].id
        developers = team[i].developers   
        cursor.execute("INSERT INTO team VALUES(?,?)", (team_id,developers))
        cursor.execute("INSERT INTO team_and_project VALUES(?,?,?,?)", (team_id,developers,None, None))
        conn.commit()


def check_idle_developers():
    idle = cursor.execute("""SELECT idle_developers FROM team_and_project
                      WHERE idle_developers IS NOT NULL
                   """)
    

@app.post("/project")
def add_project(project: Project):
    project_id = project.id
    devs_needed = project.devs_needed
    cursor.execute("INSERT INTO project VALUES(?,?)", (project_id,devs_needed))
    cursor.execute("""UPDATE team_and_project
                      SET assigned_project_id = ?
                      WHERE developers IN (SELECT developers
                                           FROM team_and_project
                                           WHERE developers >= ?
                                           ORDER BY developers
                                           LIMIT 1)
                   """, (project_id, str(devs_needed)))
    cursor.execute("""UPDATE team_and_project
                      SET idle_developers = developers - ?
                      WHERE idle_developers IS NULL AND assigned_project_id IS NOT NULL
                   """, str(devs_needed)) 

    conn.commit()
    




















