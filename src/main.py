from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.models.models
from src.api.apiV1 import routerV1
from src.auth.auth import routerAuth
from src.database.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    src.models.models.Base.metadata.create_all(bind=engine)

    yield
    # shutdown logic
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(routerV1)
app.include_router(routerAuth)
