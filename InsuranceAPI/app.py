from fastapi import FastAPI, Query,Path, HTTPException
import uvicorn
# import asyncio
from fastapi.responses import JSONResponse
from model.predict import predict_output
from schema.model import UserInput
from schema.prediction_response import PredictionResponse


app = FastAPI(
    description= "This api will pridict the insurance best suits you",
    version="1.0"
)

MODEL_VERSION= "1.0.0"

@app.get("/")
def root():
    return f"Api is working fine"

@app.get("/health")
def health():
    return {
        "status":"OK",
        "version":MODEL_VERSION
    }

@app.post("/predict",response_model=PredictionResponse)
def predict(data:UserInput):
    try:

        input_df={
            "bmi":data.bmi,
            "age_group":data.age_group,
            "lifestyle_risk":data.lifestyle_risk,
            "city_tier":data.city_tier,
            "income_lpa":data.income_lpa,
            "occupation":data.occupation
        }
        prediction= predict_output(input_df)
        return JSONResponse(status_code=200,content={"predicted_category":prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

if __name__ =="__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )