from fastapi import FastAPI, Path

import json 

app = FastAPI()

@app.get("/")
def root():
    print("This is my root function hitting the endpoint")
    with open("data.json","r") as f:
        data =json.load(f)
    return f"This is data {data}"

@app.get("/view_data/{query_parameter}")
def fetch_data(query_parameter : str = Path(...,description="This is query parameter",example="String")):
    return {"Name": "Ashmeet","Roll No": 2411414}


if  __name__=="__main__":
    unicorn.