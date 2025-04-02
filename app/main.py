from contextlib import asynccontextmanager

from app.api.routes import auth_router, posts_router
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.core.database import initialize_database, database_engine

description = """
A FastAPI project implementing all the requirements
[here](https://docs.google.com/document/d/1OdP3WeTuNvfgG79699pOaf8RNFCaouw7B8usJbJzw3o/edit?pli=1&tab=t.0)
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database(database_engine)
    yield
    await database_engine.dispose()


app = FastAPI(
    title="Lucid API", debug=settings.DEBUG, lifespan=lifespan, description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(posts_router, prefix=f"/api/{settings.API_VERSION}")


@app.get("/")
async def redirect_to_documentation():
    return RedirectResponse("/docs")
