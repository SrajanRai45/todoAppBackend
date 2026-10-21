from fastapi import APIRouter

routerAuth = APIRouter()


@routerAuth.get("/auth/")
async def get_user():
    return {"user": "authenticated"}
