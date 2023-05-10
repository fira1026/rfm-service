import os
import logging
import subprocess
import psycopg
from fastapi import FastAPI
from web.app.utils import transfer_kaggle_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

RESULT_DIR = '/home/vscode/miniproj/api/results'

@app.get("/api/hello")
async def hello():
    return {"message": "Hello World"}

@app.post("/api/rfm-analysis")
async def rfm_analysis(payload: dict):
    kaggle_file_path = payload['file_path']
    rfm_input_path = transfer_kaggle_data(kaggle_file_path)
    rfm_output_path = os.path.join(RESULT_DIR, 'rfm-segments.csv')
    logging.info('*' * 80)
    logging.info("Running subprocess with input: ", rfm_input_path)
    logging.info("Running subprocess with output: ", rfm_output_path)

    command = ["python", "/home/vscode/miniproj/api/RFM-analysis.py", "-i", rfm_input_path, "-o", rfm_output_path, "-d", "2023-05-10"]
    logging.info(f"Running subprocess with command: {' '.join(command)}")

    subprocess.run(command, capture_output=False)

    return {'file_path': rfm_output_path}
