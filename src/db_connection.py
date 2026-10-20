"""Database connection module for SQL Server (Americans Database)."""

from sqlalchemy import create_engine
import sys

def get_connection():
    """Establish and return a SQLAlchemy engine connection to the local SQL Server instance.

    Uses Windows Authentication (Trusted Connection) via ODBC Driver 17.
    """
    connection_string = (
        "mssql+pyodbc://localhost/Americans?"
        "driver=ODBC+Driver+17+for+SQL+Server&Trusted_connection=yes"
    )

    try:
        conn = create_engine(connection_string)
        print("Database connection successfully established.")
        return conn
    except Exception as e:
        print(f"Error establishing database connection: {e}", file=sys.stderr)
        return None
