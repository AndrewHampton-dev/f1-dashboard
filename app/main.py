import fastf1 as Fastf1
from app.ingest_race import ingest_laps, upsert_drivers_and_teams, upsert_race, ingest_results
import argparse
from app.database import SessionLocal
import os
from fastapi import FastAPI


app = FastAPI()


os.makedirs('fastf1_cache', exist_ok=True)
Fastf1.Cache.enable_cache('fastf1_cache')


def main(year, round_num):
    session = Fastf1.get_session(year, round_num, "R")

    session.load(weather=False, messages=False)

    circuit_info = session.get_circuit_info()
    with SessionLocal() as db:
        with db.begin():
            driver_ids, team_ids = upsert_drivers_and_teams(db, session.results)
            ingest_results(db, session, race_id, driver_ids, team_ids)
            ingest_laps(db, session, race_id, driver_ids)
    print(f"Ingested {year} round {round_num}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("round", type=int)

    args = parser.parse_args()
    main(args.year, args.round)
