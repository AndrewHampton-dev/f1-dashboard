from sqlalchemy.orm import sessionmaker
from app.schemas import ConstructorStandingRow, DriverStandingRow
from app.models import Driver, Constructor, Race, SessionResult, LapSummary
from sqlalchemy import func, case, and_, select
from sqlalchemy.orm import Session, aliased

from sqlalchemy import and_


def get_driver_by_ref(db: Session, driver_ref: str):
    return db.query(Driver).filter(Driver.driver_ref == driver_ref).first()


def create_driver(db: Session, driver_data: dict):
    db_driver = Driver(**driver_data)
    db.add(db_driver)
    db.flush()
    db.refresh(db_driver)
    return db_driver


def get_race_result(db: Session, season: int, round_num: int):
    return (
        db.query(SessionResult)
        .join(Race, SessionResult.race_id == Race.id)
        .filter(Race.season == season, Race.round_num == round_num)
        .order_by(SessionResult.position_finished)
        .all()
    )


def get_constructor_standings(db: Session, season: int) -> list[ConstructorStandingRow]:
    rows = (
        db.query(
            Constructor.name.label("team"),
            func.sum(SessionResult.points_scored).label("points"),
            func.sum(case(
                (and_(SessionResult.session_type == "Race",
                      SessionResult.position_finished == 1), 1),
                else_=0,
            )).label("wins"),
        )
        .join(Race, SessionResult.race_id == Race.id)
        .join(Constructor, SessionResult.team_id == Constructor.id)
        .filter(Race.season == season,  SessionResult.session_type.in_(["Race", "Sprint"]))
        .group_by(Constructor.name)
        .order_by(func.sum(SessionResult.points_scored).desc())
        .all()
    )
    return [
        ConstructorStandingRow(
            position=i + 1,
            team=r.team,
            points=int(r.points or 0),
            wins=r.wins,
        )
        for i, r in enumerate(rows)
    ]


def get_driver_standings(db: Session, season: int):
    LastResult = aliased(SessionResult)
    LastRace = aliased(Race)
    LastTeam = aliased(Constructor)   # alias so the subquery stays independent of the outer query

    # The team from this driver's most recent Race/Sprint result in the season
    last_team = (
        select(LastTeam.name)
        .join(LastResult, LastResult.team_id == LastTeam.id)
        .join(LastRace, LastResult.race_id == LastRace.id)
        .where(
            LastResult.driver_id == Driver.id,
            LastRace.season == season,
            LastResult.session_type.in_(["Race", "Sprint"]),
        )
        .order_by(LastRace.round_num.desc(), LastResult.id.desc())
        .limit(1)
        .correlate(Driver)
        .scalar_subquery()
    )

    rows = (
        db.query(
            Driver.full_name.label("name"),
            last_team.label("team"),
            func.sum(SessionResult.points_scored).label("points"),
            func.sum(case(
                (and_(SessionResult.session_type == "Race",
                      SessionResult.position_finished == 1), 1),
                else_=0,
            )).label("wins"),
        )
        .join(SessionResult, SessionResult.driver_id == Driver.id)
        .join(Race, SessionResult.race_id == Race.id)
        .filter(Race.season == season, SessionResult.session_type.in_(["Race", "Sprint"]))
        .group_by(Driver.id, Driver.full_name)
        .order_by(func.sum(SessionResult.points_scored).desc())
        .all()
    )
    return [
        DriverStandingRow(position=i + 1, name=r.name, team=r.team,
                          points=int(r.points or 0), wins=r.wins)
        for i, r in enumerate(rows)
    ]
