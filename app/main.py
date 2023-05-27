from fastapi import FastAPI

import models
from app.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'xd'}
