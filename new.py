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
import random


app = FastAPI()

teams = {}


projects = {}

assigned_projects = {}

team_id_idle = {}


team_projects = {}


def delete_all():
   teams.clear()


@app.get("/")
def root():
    return {"message": "Hello!"}



@app.get("/status")
def get_status():
    if (teams, projects):
        raise HTTPException(status_code=200)
    


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )



@app.put("/teams")
def put_teams(team: List[Team]):
    length = len(team)
    for i in range(length):
        team_id = team[i].id
        developers = team[i].developers
        teams[team_id] = developers
        team_id_idle[team_id] = developers
    dev_list = []
    for value in teams.values():
        dev_list.append(value)
    return teams



@app.post("/project")
def add_project(project: Project):
    projects[project.id] = project.devs_needed

    for team_id, team_devs in teams.items():

        assigned_projects1 = team_projects.get(team_id)
        assigned_projects1 = assigned_projects1 if assigned_projects1 is not None else list()
        used_devs_count = sum([projects.get(project_id) for project_id in assigned_projects1])


        if ((team_devs - used_devs_count) >= project.devs_needed):
            assigned_projects1.append(project.id)
            team_projects[team_id] = assigned_projects1
            break

    return team_projects


        


           
    
