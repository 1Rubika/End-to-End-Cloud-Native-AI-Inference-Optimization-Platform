from fastapi import FastAPI, File, UploadFile
import shutil
import os
from model import predict

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Inference Running"}

import traceback

@app.post("/predict")
def get_prediction(file: UploadFile = File(...)):
    try:
        file_path = "temp.jpg"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict(file_path)

        return {"prediction": result}

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

