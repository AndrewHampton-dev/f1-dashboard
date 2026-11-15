from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime


class ConstructorStandingRow(BaseModel):
    position: int
    team: str
    points: float
    wins: int


class DriverStandingRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    position: int
    name: str
    team: str
    points: int
    wins: int


class LeaderChallengerSummary(BaseModel):
    leader_name: str
    leader_points: int
    leader_points_gap: int

    second_challenger_name: str
    second_challenger_points: int
    second_challenger_points_gap: int

    third_challenger_name: str
    third_challenger_points: int
    third_challenger_points_gap: int


class RaceInfoSummary(BaseModel):
    race_remaining: int
    next_race: str
    next_race_date: Optional[datetime.date] = None


class HeadToHead(BaseModel):
    first_driver_name: str
    first_driver_team: str
    first_driver_points: int
    first_driver_wins: int
    first_driver_poles: int
    first_driver_dnf: int
    first_driver_avg_grid_position: float
    first_driver_avg_finish_position: float

    second_driver_name: str
    second_driver_team: str
    second_driver_points: int
    second_driver_wins: int
    second_driver_poles: int
    second_driver_dnf: int
    second_driver_avg_grid_position: float
    second_driver_avg_finish_position: float


class Driver(BaseModel):
    driver_name: str
    driver_team: str
    driver_wins: int
    driver_points: int

    driver_poles: int
    driver_dnf: int
    driver_avg_grid_position: float
    driver_avg_finish_position: float


class LapSectorAnalysis(BaseModel):
    quick_lap_time: Optional[int] = None
    quick_lap_lap_number: Optional[int] = None

    specific_lap_time: Optional[int] = None
    specific_lap_lap_number: Optional[int] = None


class HomeDashResponse(BaseModel):
    constructor_summary: LeaderChallengerSummary
    driver_summary: LeaderChallengerSummary
    race_info: RaceInfoSummary

    constructor_standings: List[ConstructorStandingRow]
    driver_standings: List[DriverStandingRow]
