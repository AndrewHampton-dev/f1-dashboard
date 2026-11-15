import os
import fastf1 as ff1
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal
from app.models import (
    Base, Constructor,Driver, Race, SessionResult, LapSummary
)
from Common import to_int, to_ms, bulk_upsert
import fastf1.Ergast


os.makedirs('fastf1_cache', exist_ok=True)
ff1.Cache.enable_cache('fastf1_cache')

def upsert_Historical_drivers_and_teams(db, results_df):
    driver_ids, team_ids = {}, {}


def upsert_historical_race(db, session, year, round_num, circuit_info):
    pass
