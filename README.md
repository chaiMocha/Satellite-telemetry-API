# 🛰️ Satellite Telemetry Ingestion API

A production-grade REST API built to simulate the continuous ingestion of high-throughput telemetry data from a constellation of satellites.

## 🚀 The Architecture
* **FastAPI:** Handles high-speed data validation and asynchronous request routing.
* **PostgreSQL (AWS RDS):** Cloud-hosted relational database for persistent data storage.
* **SQLAlchemy:** ORM layer safely translating Python schemas to SQL tables.
* **AWS EC2:** Linux (Ubuntu) server hosting the API 24/7 using Uvicorn and Systemd.
* **Security:** Endpoints locked down via API Key Header authentication.

## ⚙️ How It Works
1. A Python simulation script (`mock_stream.py`) continuously generates realistic orbital coordinates, battery degradation, and timestamps for three distinct satellites.
2. The script POSTs this JSON data to the API hosted on an AWS EC2 instance.
3. The API validates the payload via Pydantic models and writes it to an AWS RDS PostgreSQL database.
4. An authenticated GET endpoint allows querying the latest real-time status of any specific satellite.

## 🛠️ Local Development Setup
1. Clone the repository.
2. Create a virtual environment and `pip install -r requirements.txt`
3. Create a `.env` file with `DATABASE_URL` and `API_KEY` variables.
4. Run `uvicorn main:app --reload` to start the local server.

## 🧪 Testing
Includes an automated Pytest suite leveraging FastAPI's `TestClient` to verify endpoint logic and database connection integrity. Run via:
`pytest -v`