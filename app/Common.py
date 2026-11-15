import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal, engine
from app.models import (
    Base, Constructor, Driver, Race, SessionResult, LapSummary
)


def to_int(value):
    return None if pd.isna(value) else int(value)

# Fastf1 sector and lap times are in TimeDelta. pd.td -> milliseconds


def to_ms(td):
    if pd.isna(td):
        return None

    if isinstance(td, (int, float)):
        return float(td)

    return td.total_seconds() * 1000.0


def bulk_upsert(db, model, rows, conflict_cols, update_cols=None):
    if not rows:
        return
    stmt = pg_insert(model).values(rows)
    if update_cols:
        stmt = stmt.on_conflict_do_update(
            index_elements=conflict_cols,
            set_={c: stmt.excluded[c] for c in update_cols},
        )
    else:
        stmt = stmt.on_conflict_do_nothing(
            index_elements=conflict_cols
        )
    db.execute(stmt)
