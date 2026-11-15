from sqlalchemy import Integer, String, MetaData, Table, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List
from app.database import Base


class Driver(Base):
    __tablename__ = "dim_drivers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    driver_ref: Mapped[str] = mapped_column(unique=True, index=True)
    code: Mapped[Optional[str]] = mapped_column(String(3), unique=True, index=True)
    number: Mapped[int] = mapped_column(Integer)
    full_name: Mapped[str] = mapped_column(String)
    nationality: Mapped[str] = mapped_column(String)

    results: Mapped[list["SessionResult"]] = relationship("SessionResult", back_populates="driver")
    laps: Mapped[List["LapSummary"]] = relationship("LapSummary", back_populates="driver")


class Constructor(Base):
    __tablename__ = "dim_Constructor"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    results: Mapped[list["SessionResult"]] = relationship(
        "SessionResult", back_populates="constructor")


class Race(Base):
    __tablename__ = "dim_races"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    circuit_name: Mapped[str] = mapped_column(String)
    round_num: Mapped[int] = mapped_column(Integer)
    race_name: Mapped[str] = mapped_column(String)

    results: Mapped[List["SessionResult"]] = relationship("SessionResult", back_populates="race")
    laps: Mapped[List["LapSummary"]] = relationship("LapSummary", back_populates="race")


class SessionResult(Base):
    __tablename__ = "fact_session_result"
    __table_args__ = (
        UniqueConstraint("driver_id", "race_id", name="uq_result_driver_race"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    driver_id: Mapped[int] = mapped_column(ForeignKey("dim_drivers.id"), nullable=False)
    race_id:   Mapped[int] = mapped_column(ForeignKey("dim_races.id"),   nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("dim_Constructor.id"), nullable=False)

    grid_position: Mapped[Optional[int]] = mapped_column(Integer)
    position_finished: Mapped[Optional[int]] = mapped_column(Integer)
    points_scored: Mapped[Float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String)
    session_type: Mapped[Optional[str]] = mapped_column(String)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="results")
    race: Mapped["Race"] = relationship("Race", back_populates="results")
    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="results")


class LapSummary(Base):
    __tablename__ = "fact_lap_summary"
    __table_args__ = (
        UniqueConstraint("driver_id", "race_id", "session_type", "lap_number", name="uq_lap"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    driver_id:       Mapped[int] = mapped_column(ForeignKey("dim_drivers.id"), nullable=False)
    race_id:         Mapped[int] = mapped_column(ForeignKey("dim_races.id"),   nullable=False)
    session_type:    Mapped[str] = mapped_column(String)
    lap_number:      Mapped[int] = mapped_column(Integer)
    lap_time_ms:     Mapped[Optional[float]] = mapped_column(Float)  # Store as total milliseconds
    sector1_time_ms: Mapped[Optional[float]] = mapped_column(Float)
    sector2_time_ms: Mapped[Optional[float]] = mapped_column(Float)
    sector3_time_ms: Mapped[Optional[float]] = mapped_column(Float)
    tire_compound:   Mapped[Optional[str]] = mapped_column(String)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="laps")
    race: Mapped["Race"] = relationship("Race", back_populates="laps")
