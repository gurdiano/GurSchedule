from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from App.BackEnd.Entities import models
from App.BackEnd.Services import services as service
import datetime
import threading, time
import traceback

# from App.BackEnd.Seeding import Icons

# URL de conexão usando SQLAlchemy com o driver psycopg2
DATABASE_URL = "sqlite:///GurSchedule.db"
engine = create_engine(DATABASE_URL)

Base = models.Base

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

# Cria uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# # Dropa o banco de dados
# Base.metadata.drop_all(engine)

