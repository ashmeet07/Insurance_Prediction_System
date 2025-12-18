from fastapi import FastAPI, Query,Path, HTTPException
import uvicorn
import asyncio
import pandas as pd
from fastapi.responses import JSONResponse
import pickle
from pydantic import Field,BaseModel  ,computed_field
from typing import Annotated,Literal,Optional


with open("model.pkl","rb") as f:
    model = pickle.load(f)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

app = FastAPI(
    description= "This api will pridict the insurance best suits you",
    version="1.0"
)


class UserInput(BaseModel):

    age:Annotated[int,Field(...,gt=0,lt=130,description="Age of the user")]
    city:Annotated[str,Field(...,max_length=30,description="City of the user")]
    smoker:Annotated[bool,Field(...,description="Is user is a smoker or not")]
    height:Annotated[float,Field(...,gt=0,description="Height of the user")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the user")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation of the user")]
    income_lpa:Annotated[int,Field(...,description="Income of the user in LPA")]

    @computed_field()
    @property
    def bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
            if self.smoker and self.bmi > 30:
                return "high"
            elif self.smoker or self.bmi > 27:
                return "medium"
            else:
                return "low"
    @computed_field()
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    
    @computed_field()
    @property
    def verdict(self) -> str:
        if self.bmi <18:
            return "Underweight"
        elif self.bmi <25:
            return "Normal"
        else:
            return "Underweight"
    @computed_field()
    @property
    def city_tier(self) ->int:
         if self.city in tier_1_cities:
             return 1
         elif self.city in tier_2_cities:
             return 2
         else:
             return 3


@app.get("/")
def root():
    return f"Api is working fine"


@app.post("/predict")
def predict(data:UserInput):

    input_df=pd.DataFrame([{
        "bmi":data.bmi,
        "age_group":data.age_group,
        "lifestyle_risk":data.lifestyle_risk,
        "city_tier":data.city_tier,
        "income_lpa":data.income_lpa,
        "occupation":data.occupation
    }])
    prediction= model.predict(input_df)[0]
    return JSONResponse(status_code=200,content={"predicted_category":prediction})

if __name__ =="__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )