from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime

# SQLAlchemy Model (Database)
class TelemetryDB(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, index=True)
    timestamp = Column(DateTime)
    battery_level = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)

# Pydantic Schemas (API Validation)
class TelemetryCreate(BaseModel):
    satellite_id: str
    timestamp: datetime
    battery_level: float
    latitude: float
    longitude: float
    altitude: float

class TelemetryResponse(TelemetryCreate):
    id: int
    class Config:
        from_attributes = True