from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Satellite Telemetry API")

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return api_key

@app.post("/telemetry/", response_model=models.TelemetryResponse, status_code=201)
def ingest_telemetry(
    telemetry: models.TelemetryCreate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(verify_api_key) # <-- This locks the endpoint
):
    db_item = models.TelemetryDB(**telemetry.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/telemetry/{satellite_id}/latest", response_model=models.TelemetryResponse)
def get_latest_telemetry(
    satellite_id: str, 
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    record = db.query(models.TelemetryDB)\
               .filter(models.TelemetryDB.satellite_id == satellite_id)\
               .order_by(models.TelemetryDB.timestamp.desc())\
               .first()
    if not record:
        raise HTTPException(status_code=404, detail="Satellite data not found")
    return record