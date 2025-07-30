from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.db import models
from app.db.database import engine
from dotenv import load_dotenv
load_dotenv()


models.Base.metadata.create_all(bind=engine.sync_engine)

app = FastAPI(
    title="Call Analytics Service",
    version="1.0.0",
    description="Ingests call transcripts and provides analytics via REST API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api/v1")
