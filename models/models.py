from typing import List
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Text, Numeric, sql
import sqlalchemy
from dependencies.dbconnection import database, metadata

diseases: sqlalchemy.Table = sqlalchemy.Table(
    "diseases",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("treatment", sqlalchemy.Text),
    sqlalchemy.Column("symptoms", sqlalchemy.Text),
)