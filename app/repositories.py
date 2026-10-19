from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from app.models import *

def get_driver_by_ref(db: session, driver_ref: str):
	return db.query(models.Driver).filter(models.Driver.driver_ref == driver_ref)

def create_driver(db: session, driver_data: dict):
	db_driver = models.Driver(**driver_data)
	db.add(db_driver)
	db.commit()
	db.refresh(db_driver)
	return db_driver

def get_race_result(db: session, year: int, round_num: int):
	return db.query(models.SessionResult)\
			.join(models.Race)\
			.filter(models.Race.year == year, models.Race.round == round_num)\
			.all()

