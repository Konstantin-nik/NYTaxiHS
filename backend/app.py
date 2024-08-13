import uvicorn
import logging

from fastapi import FastAPI
from backend.api import router as api_v1_router

app = FastAPI(port=8000)

app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0")