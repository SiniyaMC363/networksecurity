import certifi
from dotenv import load_dotenv
import pymongo
import os
import sys
from datetime import datetime

import pandas as pd

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

from fastapi.responses import Response, FileResponse
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.staticfiles import StaticFiles

PREDICTION_OUTPUT_CSV = os.path.join("prediction_output", "output.csv")
RESULT_TABLE_MAX_ROWS = 500


ca = certifi.where()

load_dotenv()
mango_db_url = os.getenv("MONGO_DB_URL")
print(mango_db_url)


client = pymongo.MongoClient(mango_db_url, tlsCAFile=ca)


database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


@app.get("/download-report")
async def download_report():
    if not os.path.isfile(PREDICTION_OUTPUT_CSV):
        raise HTTPException(
            status_code=404, detail="No report available yet. Run a prediction first.")
    return FileResponse(
        PREDICTION_OUTPUT_CSV,
        filename="phishing_detection_report.csv",
        media_type="text/csv",
    )


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        processor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=processor, model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)

        print("Predictions:", y_pred)

        # Convert predictions into list
        df["predicted_column"] = list(y_pred)

        print(df.head())

        df['Prediction'] = df['predicted_column'].replace({
            1: "Safe",
            0: "Phishing"
        })
        safe_count = (df['Prediction'] == "Safe").sum()
        phishing_count = (df['Prediction'] == "Phishing").sum()
        total_count = len(df)

        # df['predicted_column'].replace(-1,0)
        # return df.to_json()
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv(PREDICTION_OUTPUT_CSV, index=False)

        display_df = df.drop(columns=["predicted_column"], errors="ignore")
        table_truncated = len(display_df) > RESULT_TABLE_MAX_ROWS
        table_df = display_df.head(RESULT_TABLE_MAX_ROWS)
        table_headers = [str(c) for c in table_df.columns.tolist()]
        table_rows = table_df.astype(str).values.tolist()

        safe_pct = round(100.0 * safe_count / total_count,
                         1) if total_count else 0.0
        phishing_pct = round(100.0 * phishing_count /
                             total_count, 1) if total_count else 0.0
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "request": request,
                "safe_count": int(safe_count),
                "phishing_count": int(phishing_count),
                "total_count": int(total_count),
                "safe_pct": safe_pct,
                "phishing_pct": phishing_pct,
                "table_headers": table_headers,
                "table_rows": table_rows,
                "table_truncated": table_truncated,
                "table_shown": len(table_df),
                "completed_at": completed_at,
            },
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
