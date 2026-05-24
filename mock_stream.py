import requests
import time
import random
from datetime import datetime, timezone

API_URL = "http://localhost:8000/telemetry/"

# Initial state for a small constellation
satellites = {
    "SAT-Alpha-1": {"battery": 100.0, "lat": 35.0, "lon": -100.0, "alt": 400.0},
    "SAT-Beta-2": {"battery": 95.0, "lat": 10.0, "lon": 45.0, "alt": 410.0},
    "SAT-Gamma-3": {"battery": 88.5, "lat": -20.0, "lon": 130.0, "alt": 395.0}
}

def generate_telemetry(sat_id, state):
    # Simulate realistic changes
    state["battery"] -= random.uniform(0.01, 0.1)
    if state["battery"] < 20.0:
        state["battery"] = 100.0 
        
    # Orbit shifts slightly
    state["lat"] = (state["lat"] + random.uniform(-0.5, 0.5)) % 90
    state["lon"] = (state["lon"] + random.uniform(0.5, 1.5)) % 180
    state["alt"] += random.uniform(-1.0, 1.0)
    
    return {
        "satellite_id": sat_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "battery_level": round(state["battery"], 2),
        "latitude": round(state["lat"], 4),
        "longitude": round(state["lon"], 4),
        "altitude": round(state["alt"], 2)
    }

print("Starting satellite telemetry stream... Press Ctrl+C to stop.")

try:
    while True:
        for sat_id, state in satellites.items():
            payload = generate_telemetry(sat_id, state)
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    print(f"[{payload['timestamp']}] Transmitted {sat_id} | Bat: {payload['battery_level']}% | Alt: {payload['altitude']}km")
                else:
                    print(f"Error from API: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                print("Failed to connect to API. Is Uvicorn running?")
                time.sleep(5)
                
        # Wait 2 seconds before the next transmission cycle
        time.sleep(2)

except KeyboardInterrupt:
    print("\nTelemetry stream stopped.")