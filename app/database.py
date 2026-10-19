from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import streamlit as st

conn = st.connection("postgresql", type='sql')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=conn.engine)
#st.error(f"Database connection failed: {e}")

# FastAPI dependency to handle DB sessions cleanly per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
