from fastapi import FastAPI
from pydantic import Field,BaseModel  ,computed_field
from typing import Annotated,Literal



app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str,Field(...,description="Please enter the correct patient id",example="P001")]
    name:Annotated[str,Field(...,description="Please enter the correct name",exampel="Rocky")]
    city:Annotated[str,Field(...,description="Please enter the correct city name",exampel="indore")]
    age:Annotated[int,Field(...,description="Please enter the correct name",exampel="Rocky")]
    gender:Annotated[Literal["Male","Female","Others"],Field(...,description="Please enter the correct gender",exampel="Rocky")]
    height:Annotated[float,Field(...,description="Please enter the correct height",exampel="Rocky")]
    weight:Annotated[float,Field(...,description="Please enter the correct weight",exampel="Rocky")]


    @computed_field()
    @property
    def calculate_bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field()
    @property
    def verdict(self) ->str:

        if self.calculate_bmi < 18.5:
            return "under weight"
        elif self.calculate_bmi <25:
            return "Normal"
        else :
            return "Over weight"
        

