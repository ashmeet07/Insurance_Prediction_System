from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal
from config.config_city import tier_1_cities,tier_2_cities



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
