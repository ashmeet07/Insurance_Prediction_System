from pydantic import BaseModel, EmailStr, AnyUrl, Field,field_validator,model_validator
from typing import List, Dict,Optional,Annotated

#Anotated is use to set the meta deta of the api

class Patient(BaseModel):

    name : str 
    email:EmailStr
    # url: AnyUrl
    age : int 
    # things: List[str]
    # values:Dict[str,any]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):

        valid_domain=['hdfc.com","icici.com']
        domain_name=value.split("@")[-1]
        if domain_name in valid_domain:
            raise ValueError("Not in valid domains")

        return value
    # @field_validator('age',mode="before")
    # @classmethod
    # def age_validator(cls,value):
    #     if  0<value<100:
    #         return value
    #     else :
    #         raise ValueError("The age is note in between 0 to 100 ")


    @model_validator(mode='after')
    def mode_validate(cls,model):
        if model.age>65:
            print("Enter correct age")
        return model
        
    



def insert_data(paitient:Patient):

    print(paitient.email)
    print(f"performing data validation")

paitient={"name":"ashmeet","age":8, "email":"ashmeet@hdfc.com"}

patient=Patient(**paitient)


insert_data(patient)


#in filed validator you only can custom validate the given field but if you want to validate multiple field then you have to use model validator okay