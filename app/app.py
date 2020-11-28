from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api_v1.api import api_router
from .api.common.api import api_router as common_api_router
from .storage.db import database

app = FastAPI(docs_url="/")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1",
    "http://localhost:8080",
    "https://pft-webapp.herokuapp.com",
]

app.add_middleware(
CORSMiddleware,
    allow_origins=origins, # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(common_api_router)
app.include_router(api_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
