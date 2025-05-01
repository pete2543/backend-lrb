
from fastapi import FastAPI
from app.api.v1 import district,gensubscribe

app = FastAPI()

app.include_router(district.router);
app.include_router(gensubscribe.router);
