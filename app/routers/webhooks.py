from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.post("/intraservice/request_closed")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        # Process the webhook payload here
        return {"status": "success", "message": "Webhook received"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {e}")