class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1424@localhost/SistemaFacturacion'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from flask import Flask
from models import db
from config import Config



