from fastapi import APIRouter

auth_router =  APIRouter(prefix="/auth",tags=["User Authentication"])


@auth_router.post('/sign-up')
async def sign_up():
    ...

@auth_router.post('/login')
async def login():
    ...