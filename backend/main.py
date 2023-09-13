from fastapi import FastAPI
from backend import utils


utils = utils.Utils()
app = FastAPI()


@app.get("/{name}")
def predict(name: str):
    
    data = utils.predict(name=name)
    return {'data':data}