from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TelemetryDB(Base):
    __tablename__ = "telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, index=True)
    timestamp = Column(DateTime)
    battery_level = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)

class TelemetryCreate(BaseModel):
    satellite_id: str
    timestamp: datetime
    battery_level: float
    latitude: float
    longitude: float
    altitude: float

class TelemetryResponse(TelemetryCreate):
    id: int
    status: Optional[str] = None

    def model_post_init(self, __context) -> None:
        if self.battery_level is not None:
            if self.battery_level < 15:
                self.status = "CRITICAL"
            elif self.battery_level < 40:
                self.status = "WARNING"
            else:
                self.status = "NOMINAL"

    class Config:
        from_attributes = True