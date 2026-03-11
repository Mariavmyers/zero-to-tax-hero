import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

# 1. Setup Security - This tells the API to look for the "access_token" header
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    # This checks the "Vault" you just updated in Render
    if api_key == os.getenv("API_KEY"):
        return api_key
    raise HTTPException(status_code=403, detail="Forbidden: Invalid Hero Key")

app = FastAPI()

# 2. Define the data structure
class TaxRequest(BaseModel):
    year: int
    mars: int  # 1 for Single, 2 for Married
    wages_p: float
    wages_s: float = 0

@app.get("/")
def read_root():
    return {"message": "The Hero API is live, but the door is locked for your protection!"}

@app.post("/estimate")
def estimate_tax(data: TaxRequest, api_key: str = Depends(get_api_key)):
    total_income = data.wages_p + data.wages_s
    # MainEntry LLC Logic: 15% Estimated Tax
    estimated_tax = total_income * 0.15
    
    return {
        "year": data.year,
        "total_income": total_income,
        "estimated_tax": estimated_tax,
        "status": "Success",
        "message": "Calculated by MainEntry LLC logic."
    }
