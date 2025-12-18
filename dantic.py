from pydantic import BaseModel, EmailStr, AnyUrl, Field,computed_field
from typing import List, Dict,Optional,Annotated,Any

#Anotated is use to set the meta deta of the api
class Address(BaseModel):
    city:str
    state:str
    pincode:int

class Patient(BaseModel):

    name : Optional[str] = None 
    email:Annotated[EmailStr,Field(max_length=50,title="This is email field",description="Please enter you email which is grea")]
    url: Annotated[AnyUrl,Field(title="url check")]
    age : int =Field(gt=0) # now no one send the data which is less than 0
    things: List[str]
    values:Dict[str,Any]
    weight: int  #KG
    height:float  #CM 
    address:Address

    @computed_field
    @property
    def computed_one(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi



def insert_data(paitient:Patient):

    print(paitient.name,paitient.age,paitient.computed_one)
    print(f"performing data validation")

address={"city":"indore","state":"madhya pradesh","pincode":452001}
address1=Address(**address)
paitient={"name":"ashmeet","email":"ashmeet@gmail.com","url":"https://linkedin.com/ashmeet07","things":["ashmeet","singh","how ","are","you"],"values":{"hello":1,"world":2},"age":20,"weight":90,"height":1.72,"address":address1}

patient=Patient(**paitient)

temp = patient.model_dump(exclude={"address": {"state"}})#export only selected fields inlcud=['name']
temp = patient.model_dump(exclude_unset=True)#at the time of object creation the things which are not set will not export 
temp2 = patient.model_dump_json()
print(temp,type(temp))
print(temp2,type(temp2))
insert_data(patient)