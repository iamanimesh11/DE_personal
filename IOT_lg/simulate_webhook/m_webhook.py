from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define the expected request body
class Report(BaseModel):
    error: Optional[str] = None


class Event(BaseModel):
    deviceId: str = "Unknown"
    pushType: str = "Unknown"
    deviceType: str = "Unknown"
    report: Report = Report()


class DeviceEvent(BaseModel):
    event: Event


@app.post("/device-event")
async def receive_device_event(event: DeviceEvent):
    try:
        device_id = event.event.deviceId
        event_type = event.event.pushType
        report = event.event.report
        # device_type = event.event.deviceType  # This will be "Refrigerator", "AC", etc.


        logger.info(f"📩 Received event: {event}")

        # Check for errors
        if report.error:
            error_message = report.error
            logger.error(f"🚨 Error in {device_id}: {error_message}")
            return {"status": "error received"}

        logger.info(f"✅ Normal event from {device_id} : {report}")
        return {"status": "success"}

    except Exception as e:
        logger.exception(f"❌ Error processing event: {e}")
        raise HTTPException(status_code=500, detail=str(e))
