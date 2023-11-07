import os
import pandas
from dotenv import load_dotenv
from sqlalchemy import create_engine, QueuePool, text
from sqlalchemy.engine import URL

from api.query_builder import QueryBuilder

load_dotenv()

url = URL.create(
    drivername=os.getenv("SQL_DRIVER"),
    username=os.getenv("SQL_DATABASE_USER"),
    password=os.getenv("SQL_DATABASE_PASSWORD"),
    host=os.getenv("SQL_DATABASE_HOSTNAME"),
    port=os.getenv("SQL_DATABASE_PORT"),
    database=os.getenv("SQL_DATABASE")
)

engine = create_engine(url)
connection = engine.connect()


def db_select(selection: str, table: str, conditions: str):
    if not table:
        return
    builder = "SELECT "
    if selection:
        builder += selection
    else:
        builder += "*"

    builder += " FROM "
    builder += table

    if conditions:
        builder += " WHERE "
        builder += conditions

    builder += ";"
    result = connection.execute(text(builder))
    return result.fetchall()


def db_dataframe(selection: str, table: str, conditions: str):
    if not table:
        return

    builder = "SELECT "
    if selection:
        builder += selection
    else:
        builder += "*"

    builder += " FROM "

    if conditions:
        builder += conditions

    df_engine = create_engine(url, poolclass=QueuePool, pool_size=10, max_overflow=20)
    con = df_engine.connect()

    result = con.execute(text(builder))
    df = pandas.DataFrame(result.fetchall())
    df.columns = result.keys()
    return df


def db_querybuilder(query: QueryBuilder()):
    print(query.build())
    result = connection.execute(text(query.build()))
    return result.fetchall()


def db_querybuilder_dataframe(query: QueryBuilder()):
    df_engine = create_engine(url, poolclass=QueuePool, pool_size=10, max_overflow=20)
    con = df_engine.connect()

    result = con.execute(text(query.build()))
    df = pandas.DataFrame(result.fetchall())
    df.columns = result.keys()
    return df
