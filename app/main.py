
from fastapi import FastAPI
from app.api.v1 import district

app = FastAPI()

app.include_router(district.router)
