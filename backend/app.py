from fastapi import FastAPI
import uvicorn
from api import router as api_v1_router

app = FastAPI(port=8000)

app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")