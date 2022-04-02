from pickle import LIST
from typing import List
from xmlrpc.client import boolean
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import *
from pydantic import BaseModel
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
import logging


meta_data_obj = MetaData()
meta_data_obj1 = MetaData()
meta_data_obj2 = MetaData()


project = Table('project', meta_data_obj,
    Column('id', Integer, primary_key=True),
    Column('devs_needed', Integer, nullable=False)
    )


team = Table('team', meta_data_obj1,
    Column('id', Integer, primary_key=True),
    Column('developers', Integer, nullable=False)
    )


team_and_project = Table('team_and_project', meta_data_obj2,
    Column('team_id', Integer),
    Column('developers', Integer),
    Column('idle_developers', Integer),
    Column('assigned_project_id', String),
)


class Project(BaseModel):
    id: int
    devs_needed: int


class Team(BaseModel):
    id: int
    developers: int