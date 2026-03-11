from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Maria Tax API")

class EstimateRequest(BaseModel):
    year: int
    mars: int
    wages_p: float
    wages_s: float = 0

@app.get("/")
def home():
    return {"message": "Zero-to-Tax-Hero API is Live!"}

@app.post("/estimate")
def estimate(data: EstimateRequest):
    # This is where your hero logic begins!
    total_wages = data.wages_p + data.wages_s
    return {
        "year": data.year,
        "total_income": total_wages,
        "status": "Success",
        "message": "Win for the curiosity of a 5-year old!"
    }
