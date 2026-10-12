from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.apiV1 import routerV1
from database.database import engine
import models.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    models.models.Base.metadata.create_all(bind=engine)

    yield
    # shutdown logic
    engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(routerV1)
