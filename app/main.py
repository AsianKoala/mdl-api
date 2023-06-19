from core.log import generate_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import FlattenQueryStringListMiddleware

from app.routers import drama
from app.routers import genres
from app.routers import tags

logger = generate_logger()
logger.info("Starting API")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.add_middleware(FlattenQueryStringListMiddleware)

app.include_router(drama.router)
app.include_router(genres.router)
app.include_router(tags.router)


@app.get("/")
async def root():
    return {"message": "wsg"}
