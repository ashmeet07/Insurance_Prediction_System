from fastapi import FastAPI, Query,Path, HTTPException
import uvicorn
import asyncio
from fastapi.responses import JSONResponse
import json
from pydantic import Field,BaseModel  ,computed_field
from typing import Annotated,Literal,Optional


app = FastAPI(
    description="This is the api for assignment purpose",
    version="1.0"
)

def load_data():
     with open("data.json",'r') as f:
        data = json.load(f)
        return data
     
def save_data(data):
    with open("data.json","w") as f :
        json.dump(data,f)
        

class Patient(BaseModel):

    id : Annotated[str,Field(...,description="Please enter the correct patient id",example="P001")]
    name:Annotated[str,Field(description="Please enter the correct name",exampel="Rocky")]
    city:Annotated[str,Field(description="Please enter the correct city name",exampel="indore")]
    age:Annotated[int,Field(description="Please enter the correct name",exampel="Rocky")]
    gender:Annotated[Literal["Male","Female","Others"],Field(description="Please enter the correct gender",exampel="Rocky")]
    height:Annotated[float,Field(description="Please enter the correct height",exampel="Rocky")]
    weight:Annotated[float,Field(description="Please enter the correct weight",exampel="Rocky")]


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
        
class PatientUpdate(BaseModel):

    id : Annotated[Optional[str],Field(description="Please enter the correct patient id",example="P001")]
    name:Annotated[Optional[str],Field(description="Please enter the correct name",exampel="Rocky")]
    city:Annotated[Optional[str],Field(description="Please enter the correct city name",exampel="indore")]
    age:Annotated[Optional[int],Field(description="Please enter the correct name",exampel="Rocky")]
    gender:Annotated[Optional[Literal["Male","Female"]],Field(description="Please enter the correct gender",exampel="Rocky")]
    height:Annotated[Optional[float],Field(description="Please enter the correct height",exampel="Rocky")]
    weight:Annotated[Optional[float],Field(description="Please enter the correct weight",exampel="Rocky")]
        
@app.get("/")
def root():
    return f"Api is working perfectly"


@app.get("/get_data/{path_parameter}")
def fetch(path_parameter : str = Path(...,description="This is path parameter you need to enter and it is required")):
    with open("data.json","r") as f:
            data=json.load(f)
    if path_parameter in data :
        return data[path_parameter]
    raise HTTPException(status_code=404,detail=f"Data not found")



@app.get("/sort")
async def sort(sort_by : str = Query(...,description="Sort on the basis of bmi height and weight"),order : str = Query('asc',description="You have to put the asc for ascendind and for decending")):
     valid_fields=["height","weight","bmi"]
     if sort_by not in valid_fields:
          raise HTTPException(status_code=404,detail="Not present in the data and entering wrong details")
     if order not in ['asc','dsc']:
          raise HTTPException(status_code=404,detail="Not present in the data and entering wrong details")
     with open("data.json","r") as f: data=json.load(f)

     sort_order= True if order == "desc" else False
     await asyncio.sleep(2)
     sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
     
     return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
     
     #load data from database
     data =load_data()

     #Check patient from the database
     if patient.id in data:
         raise HTTPException(status_code=400,detail="Patient already is in the database")
     
     data[patient.id] =patient.model_dump(exclude=['id'])

     save_data(data)

     return JSONResponse(status_code=200,content={"message":"Patient created successfully"})

@app.put("/update/{patient_id}")
def  updatePatient(patient_id:str,patient :PatientUpdate) :

    data =load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Not Available")
    

    existing = data[patient_id]
    details=patient.model_dump(exclude_unset=True)

    for key, value in details.items():
        existing[key]=value
    
    existing["id"] = patient_id
    patient_update = Patient(**existing)

    existing=patient_update.model_dump(exclude='id')
    
    data[patient_id]=existing

    save_data(data)

    return JSONResponse(status_code=200, content="Successfully updated the data")



@app.delete("/delete/{patient_id}")
def  deletePatient(patient_id : str):
    data =load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not exist")
    

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={"message":"Patient deleted sucessfully"})


#RunServer
if __name__ =="__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )