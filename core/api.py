from fastapi import FastAPI
from core.state import get_state
from core.sampler import start_sampler
from pydantic import BaseModel
from datetime import datetime
import threading

app = FastAPI()

class SensorData(BaseModel):
    sensor_ready: bool
    last_update: datetime | None
    uptime: float | None
    turbidity: float | None
    temperature: float | None
    total_dissolved_solids: float | None
    pH: float | None

@app.get("/read", response_model=SensorData)
async def read() -> SensorData:
    return get_state()

@app.on_event("startup")
async def startup_event():
    # Start the daemon in a separate thread
    daemon_thread = threading.Thread(target=start_sampler)
    daemon_thread.daemon = True
    daemon_thread.start()
