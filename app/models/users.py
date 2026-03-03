from .base_model import BaseModel
import datetime
from peewee import AutoField, CharField, DateTimeField


class User(BaseModel):
    id = AutoField()
    name = CharField()
    email = CharField(unique=True)
    matricula = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


