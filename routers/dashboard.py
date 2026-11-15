from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import repositories
from app.schemas import HomeDashboardResponse, ConstructorStandingRow,
DriverStandingRow, LeaderChallengerSummary, RaceInfoSummary

router = APIRouter()

@router.get("/frontend/home", response_model= HomeDashboardResponse)
def get_constructor_standings(season: int, db: Session = Depends(get_db)):
    constructor_standings_db = repositories.get_constructor_standings(db)
    return constructor_standings_db
