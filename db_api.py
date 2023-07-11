import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

# Load environment variables
# load_dotenv()

# SQLite doesn't require username, password, and host like other databases
# So we directly connect to the SQLite database file
database_path = os.getenv("SQLITE_DATABASE_PATH")
engine = create_engine(f'sqlite:///{database_path}')
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
    builder += table

    if conditions:
        builder += " WHERE "
        builder += conditions

    builder += ";"
    result = connection.execute(text(builder))
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    return df
