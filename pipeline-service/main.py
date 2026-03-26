from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import migrate_models
from services.ingestion import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    migrate_models()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
