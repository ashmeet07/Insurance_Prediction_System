from pydantic import BaseModel,Field 
from typing import Dict


class PredictionResponse(BaseModel):
    predicted_category :str = Field(...,description="The predicted insurance premium category")
    confidence:float = Field(..., description="Model confidence score range(0 - 1)")
    class_probablities:Dict[str,float] = Field(..., description="Probablities distribution among all possible classes", example={"low":0.01,"medium":0.15,"high":0.84})
