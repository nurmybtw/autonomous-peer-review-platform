from fastapi import FastAPI
from routes import classification
from routes import ranking

app = FastAPI()

app.include_router(classification.router, prefix="/classification", tags=["classification"])
app.include_router(ranking.router, prefix="/ranking", tags=["ranking"])

