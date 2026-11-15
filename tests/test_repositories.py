from app.models import Driver, Constructor, Race, SessionResult, LapSummary
from app.repositories import create_driver, get_driver_by_ref, get_race_result, get_constructor_standings, get_driver_standings
from sqlalchemy.exc import IntegrityError, DataError, StatementError
import pytest

SEASON = 2025

# ---Mock Data----------------------------------------------------------------------------
DRIVERS = [
    {"driver_ref": "norris", "code": "NOR", "number": "4",
     "full_name": "Lando Norris", "nationality": "British"},
    {"driver_ref": "verstappen", "code": "VER", "number": 1,
     "full_name": "Max Verstappen", "nationality": "Dutch"},
    {"driver_ref": "leclerc", "code": "LEC", "number": 16,
     "full_name": "Charles Leclerc", "nationality": "Monegasque"},
]

CONSTRCUTOR = ["McLaren", "Red Bull", "Ferrari"]

RACES = [
    {"season": SEASON, "round_num": 4, "race_name": "Bahrain Grand Prix",
     "circuit_name": "Sakhir"},
    {"season": SEASON, "round_num": 20, "race_name": "Brazilian Grand Prix",
     "circuit_name": "Interlagos"}
]

# (driver_ref, race_index, grid, finish, points, status, team, session_type)
RESULTS = [
    ("norris",      0, 2, 1, 25.0, "finished", "McLaren", "Race"),
    ("verstappen",  0, 1, 2, 18.0, "finished", "Red Bull", "Race"),
    ("leclerc",     0, 3, 3, 15.0, "finished", "Ferrari", "Race"),
    ("verstappen",  1, 1, 1, 25.0, "finished", "Red Bull", "Race"),
    ("leclerc",     1, 1, 2, 18.0, "finished", "Ferrari", "Race"),
    ("norris",      1, 3, 3, 15.0, "finished", "McLaren", "Race"),
]


# Expected after these two races:
#   Drivers:      VER 43 (1 win), NOR 40 (1 win), LEC 33 (0 wins)
#   Constructors: Red Bull 43, McLaren 40, Ferrari 33
@pytest.fixture
def World(db_session):
    teams = {}
    for name in CONSTRCUTOR:
        team = Constructor(name=name)
        db_session.add(team)
        teams[name] = team
    db_session.flush()
    drivers = {}
    for data in DRIVERS:
        driver = Driver(**data)
        db_session.add(driver)
        drivers[data["driver_ref"]] = driver

    db_session.flush()

    races = []
    for r in RACES:
        race = Race(**r)
        db_session.add(race)
        races.append(race)
    db_session.flush()

    for driver_ref, race_idx, grid, finish, points, status, team, session_type in RESULTS:
        db_session.add(
            SessionResult(
                driver_id=drivers[driver_ref].id,
                race_id=races[race_idx].id,
                grid_position=grid,
                position_finished=finish,
                points_scored=points,
                status=status,
                team_id=teams[team].id,
                session_type=session_type
            )
        )
    db_session.flush()
    return {"drivers": drivers, "teams": teams, "races": races}


# -----driver create/get ---------------------------------------------------------------------------------
VALID_DRIVER = DRIVERS[0]

INVALID_DRIVER = {
    "driver_ref": "ver",
    "number": "not an int",
    "full_name": "Max Verstappen",
    "nationality": "Dutch",
}

EMPTY_DRIVER = {}


def test_create_Driver(db_session):
    driver = create_driver(db_session, VALID_DRIVER)
    assert driver is not None
    assert driver.full_name == "Lando Norris"


def test_get_Driver_by_ref(db_session):
    create_driver(db_session, VALID_DRIVER)
    assert get_driver_by_ref(db_session, "norris").full_name == "Lando Norris"


def test_get_Driver_by_ref_missing_returns_none(db_session):
    assert get_driver_by_ref(db_session, "HAM") is None


def test_create_Driver_Empty_raises(db_session):
    with pytest.raises(IntegrityError):
        create_driver(db_session, EMPTY_DRIVER)


def test_create_Driver_duplicate_code_raises(db_session):
    create_driver(db_session, VALID_DRIVER)
    with pytest.raises(IntegrityError):
        create_driver(db_session, {**VALID_DRIVER, "driver_ref": "someone_else"})


def test_create_Driver_invalid_number_raises(db_session):
    with pytest.raises((DataError, StatementError)):
        create_driver(db_session, INVALID_DRIVER)


def test_create_driver_duplicate_ref_raises(db_session):
    create_driver(db_session, VALID_DRIVER)
    with pytest.raises(IntegrityError):
        create_driver(db_session, VALID_DRIVER)

# --- race results ------------------------------------------------------------


def test_get_race_result(World, db_session):
    rows = get_race_result(db_session, SEASON, 4)
    assert len(rows) == 3
    assert [r.position_finished for r in rows] == [1, 2, 3]
    finishers = {r.driver.full_name: r.position_finished for r in rows}
    assert finishers == {
        "Lando Norris": 1,
        "Max Verstappen": 2,
        "Charles Leclerc": 3,

    }


def test_get_race_result_unknown_round_returns_empty(World, db_session):
    assert get_race_result(db_session, SEASON, 99) == []


def test_get_race_result_unknown_season_returns_empty(World, db_session):
    assert get_race_result(db_session, 1999, 1) == []


def test_get_driver_standings_points_and_order(World, db_session):
    rows = get_driver_standings(db_session, SEASON)
    assert [(r.position, r.name, r.points) for r in rows[:3]] == [
        (1, "Max Verstappen", 43),
        (2, "Lando Norris", 40),
        (3, "Charles Leclerc", 33),
    ]


def test_get_driver_standings_counts_wins(World, db_session):
    rows = get_driver_standings(db_session, SEASON)
    wins = {r.name: r.wins for r in rows}
    assert wins["Max Verstappen"] == 1
    assert wins["Lando Norris"] == 1
    assert wins["Charles Leclerc"] == 0


def test_get_driver_standings_total_points(World, db_session):
    """Guard against NULL points silently dropping from the SUM function"""
    rows = get_driver_standings(db_session, SEASON)
    assert sum(r.points for r in rows) == 116


def test_get_driver_standings_unknown_season_empty(World, db_session):
    assert get_driver_standings(db_session, 1999) == []


# def test_get_constructor_standings(World, db_session):
#    rows = get_constructor_standings(db_session, SEASON)
#    assert [(r.position, r.team, r.points) for r in rows[:3]] == [
#        (1, "Red Bull", 43),
#        (2, "McLaren", 40),
#        (3, "Ferrari", 33)
#    ]


def test_get_constructor_standings_unknown_season_empty(World, db_session):
    assert get_constructor_standings(db_session, 1999) == []


def test_database_is_empty_without_world_fixture(db_session):
    """Proves the rollback works"""
    assert get_driver_by_ref(db_session, "norris") is None


def test_debug(World, db_session):
    from app.models import Driver, SessionResult
    rows = (
        db_session.query(
            Driver.full_name, SessionResult.race_id,
            SessionResult.session_type, SessionResult.position_finished,
            SessionResult.points_scored,
        )
        .join(SessionResult, SessionResult.driver_id == Driver.id)
        .filter(Driver.full_name == "Max Verstappen")
        .all()

    )
    for r in rows:
        print(r)
