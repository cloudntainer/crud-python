import pytest
import os
import psycopg2


@pytest.fixture(scope="session")
def postgres_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost"
    )
    yield conn
    conn.close()
