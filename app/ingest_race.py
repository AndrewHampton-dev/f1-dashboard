import os
import fastf1 as ff1
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal
from app.models import (
    Base, Constructor,Driver, Race, SessionResult, LapSummary
)
from Common import to_int, to_ms, bulk_upsert

os.makedirs('fastf1_cache', exist_ok=True)
ff1.Cache.enable_cache('fastf1_cache')

def upsert_drivers_and_teams(db, results_df):
    driver_ids, team_ids = {}, {}

    for row in results_df.itertuples():
        driver = db.query(Driver).filter_by(driver_ref=row.DriverId).one_or_none()
        if driver is None:
            driver = Driver(

                driver_ref=row.DriverId,
                code= row.Abbreviation,
                number= to_int(row.DriverNumber),
                full_name = row.FullName,
                nationality= "",
            )
            db.add(driver)
            db.flush()
        else:
            driver.number = to_int(row.DriverNumber)
            driver.full_name = row.FullName
        driver_ids[row.Abbreviation] = driver.id

        if row.TeamName not in team_ids:
            team = db.query(Constructor).filter_by(name=row.TeamName).one_or_none()
            if team is None:
                team = Constructor(name=row.TeamName)
                db.add(team)
                db.flush()
            team_ids[row.TeamName] = team.id
    return driver_ids, team_ids

def upsert_race(db, session, year, round_num, circuit_info):
    race = db.query(Race).filter_by(season=year, round_num=round_num).one_or_none()
    if race is None:
        race = Race(
            season=year,
            round_num=round_num,
            race_name= session.event["EventName"],
            circuit_name = session.event['Location']
        )
        db.add(race)
        db.flush()
    return race.id
def ingest_results(db, session, race_id, driver_ids, team_ids):
    rows = []
    for r in session.results.itertuples():
        rows.append(
            {
                "driver_id": driver_ids[r.Abbreviation],
                "race_id": race_id,
                "team_id": team_ids[r.TeamName],
                "grid_position": to_int(r.GridPosition),
                "position_finished": to_int(r.Position), # NaN => DNF/NC => None
                "points_scored": 0.0 if pd.isna(r.Points) else float(r.Points),
                "status": None if pd.isna(r.Status) else str(r.Status),
            })
    bulk_upsert(
        db, SessionResult, rows,
        conflict_cols=["driver_id", "race_id"],
        update_cols=["position_finished", "points_scored", "status", "team_id"]
    )

def ingest_laps(db, session, race_id, driver_ids):
    laps = session.laps
    rows = []
    for lap in laps.itertuples():
        if pd.isna(lap.LapTime):
            continue
        rows.append(
            {
                "driver_id": driver_ids[lap.Driver],
                "race_id": race_id,
                "lap_number": int(lap.LapNumber),
                "lap_time_ms": to_ms(lap.LapNumber),
                "sector1_time_ms": to_ms(lap.Sector1Time),
                "sector2_time_ms": to_ms(lap.Sector2Time),
                "sector3_time_ms": to_ms(lap.Sector3Time),
                "tire_compound": None if pd.isna(lap.Compound) else lap.Compound,
            }
        )
    #Batching because while Lap data is ~1200 rows/races, the seasons can get big
    BATCH = 5000
    for i in range(0, len(rows), BATCH):
        bulk_upsert(
            db, LapSummary, rows[i:1 + BATCH],
            conflict_cols= ["driver_id", "race_id", "lap_number"],
        )
