from fastapi import APIRouter

from app.schema import SignUpSchema, SignInSchema

auth_router = APIRouter(prefix="/auth", tags=["User Authentication"])


@auth_router.post("/sign-up")
async def sign_up(body: SignUpSchema):
    raise NotImplementedError("This endpoint is yet to  be implemented")


@auth_router.post("/login")
async def login(body: SignInSchema):
    raise NotImplementedError("This endpoint is yet to  be implemented")
