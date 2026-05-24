from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Satellite Telemetry API")

@app.post("/telemetry/", response_model=models.TelemetryResponse, status_code=201)
def ingest_telemetry(telemetry: models.TelemetryCreate, db: Session = Depends(get_db)):
    db_item = models.TelemetryDB(**telemetry.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/telemetry/{satellite_id}/latest", response_model=models.TelemetryResponse)
def get_latest_telemetry(satellite_id: str, db: Session = Depends(get_db)):
    record = db.query(models.TelemetryDB)\
               .filter(models.TelemetryDB.satellite_id == satellite_id)\
               .order_by(models.TelemetryDB.timestamp.desc())\
               .first()
    if not record:
        raise HTTPException(status_code=404, detail="Satellite data not found")
    return record