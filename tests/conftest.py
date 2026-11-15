import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL or "test" not in TEST_DATABASE_URL:
    pytest.exit("Refusing to run: TEST_DATABASE_URL missing or not a test DB")


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)
    yield session

    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()
