from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import drama, genres, tags

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:8080",
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drama.router)
app.include_router(genres.router)
app.include_router(tags.router)

@app.get('/')
async def root():
    return {'message': 'xd'}
