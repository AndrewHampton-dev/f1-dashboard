from sqlalchemy import Integer, String, MetaData, Table, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional 

class Base(DeclarativeBase):
    pass

class Driver(Base):
   __tablename__  = "dim_drivers"
   id: Mapped[int] = mapped_column(primary_key=True, index=True)
   driver_ref: Mapped[str] = mapped_column(unique=True, index=True)
   code: Mapped[str] = mapped_column(String(3), unique=True, index=True)
   number: Mapped[int] = mapped_column(Integer)
   full_name: Mapped[str] = mapped_column(String)
   team: Mapped[str] = mapped_column(String)
   nationality: Mapped[str] = mapped_column(String)

   results: Mapped[list["SessionResult"]] = relationship("SessionResult", back_populates="driver")
   laps: Mapped[List["LapSummary"]] = relationship("LapSummary", back_populates="driver")

class Race(Base):
   __tablename__ = "dim_races"
   id: Mapped[int] = mapped_column(primary_key= True, index=True)
   season: Mapped[int] = mapped_column(Integer, index=True)
   circuit_name: Mapped[str] = mapped_column(String)
   round_num: Mapped[int] = mapped_column(Integer)
   race_name: Mapped[str] = mapped_column(String)

   results: Mapped[List["SessionResult"]] = relationship("SessionResult", back_populates="race")
   laps: Mapped[List["LapSummary"]] = relationship("LapSummary", back_populates="race")



class SessionResult(Base):
   __tablename__  = "fact_session_result"
   id: Mapped[int] = mapped_column(primary_key=True, index=True)

   driver_id: Mapped[int]   = mapped_column(ForeignKey("dim_drivers.id"), nullable=False)
   race_id:   Mapped[int]   = mapped_column(ForeignKey("dim_races.id"),   nullable=False)

   grid_position: Mapped[int] = mapped_column(Integer)
   position_finished: Mapped[int] = mapped_column(Integer)
   points_scored: Mapped[int] = mapped_column(Integer)
   status: Mapped[str] = mapped_column(String)



   driver: Mapped["Driver"] = relationship("Driver", back_populates="race")
   race: Mapped["Race"] = relationship("Race", back_populates="race")  



class LapSummary(Base):
   __tablename__= "fact_lap_summary"
   id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

   driver_id: Mapped[int] = mapped_column(ForeignKey("dim_drivers.id"), nullable=False)
   race_id:  Mapped[int]  = mapped_column(ForeignKey("dim_races.id"),   nullable=False)

   laps_number:     Mapped[int] = mapped_column(Integer)
   laps_time_ms:    Mapped[Optional[float]] = mapped_column(Float)  # Store as total milliseconds
   sector1_time_ms: Mapped[Optional[float]] = mapped_column(Float)
   sector2_time_ms: Mapped[Optional[float]] = mapped_column(Float)
   sector3_time_ms: Mapped[Optional[float]] = mapped_column(Float)
   tire_compound:   Mapped[Optional[str]] = mapped_column(String)

   driver: Mapped["Driver"] = relationship("Driver", back_populates="laps")
   race: Mapped["Race"] = relationship("Race", back_populates="laps")  


