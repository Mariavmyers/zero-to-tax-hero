import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

# This is the name of the "Security Badge" the user must show
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# This pulls your secret password from Render's vault
API_KEY = os.environ.get("API_KEY")

app = FastAPI(title="Zero-to-Tax-Hero Protected API")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    # If the key is wrong, they get hit with the "NO" you used to hear!
    raise HTTPException(status_code=403, detail="Forbidden: You need the Hero Key to enter.")

class EstimateRequest(BaseModel):
    year: int
    mars: int
    wages_p: float
    wages_s: float = 0

@app.get("/")
def home():
    return {"message": "The Hero API is live, but the door is locked for your protection!"}

@app.post("/estimate", dependencies=[Depends(get_api_key)])
def estimate(data: EstimateRequest):
    total_wages = data.wages_p + data.wages_s
    # Keeping your 15% estimate logic
    est_tax = total_wages * 0.15 
    return {
        "year": data.year,
        "total_income": total_wages,
        "estimated_tax": est_tax,
        "status": "Secure Access Granted",
        "message": "Win for the curiosity of a 5-year old!"
    }
