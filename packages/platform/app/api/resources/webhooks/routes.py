from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/twilio")
async def twilio_webhook():
    return {"message": "Twilio webhook received"}
