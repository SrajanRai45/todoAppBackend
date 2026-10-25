from contextlib import asynccontextmanager

from fastapi import FastAPI

import models.models
from api.apiV1 import routerV1
from auth.auth import routerAuth
from database.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    models.models.Base.metadata.create_all(bind=engine)

    yield
    # shutdown logic
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(routerV1)
app.include_router(routerAuth)
