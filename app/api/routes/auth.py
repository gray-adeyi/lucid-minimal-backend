from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_user_from_form_data, create_user_from_signup
from app.schema import TokenSchema, ResponseSchema, SignUpSchema

auth_router = APIRouter(prefix="/auth", tags=["User Authentication"])


@auth_router.post("/sign-up/")
async def sign_up(
    body: SignUpSchema,
    tokens: Annotated[
        TokenSchema, Depends(TokenSchema.generate_tokens(create_user_from_signup))
    ],
):
    """Sign up to  Lucid"""
    return ResponseSchema(detail="user signup successful", data=tokens)


@auth_router.post("/login/")
async def login(
    tokens: Annotated[
        TokenSchema, Depends(TokenSchema.generate_tokens(get_user_from_form_data))
    ],
):
    """Obtain access token to access protected resources.

    Note:
        The email address of the user should be passed as the username in the
        form data sent to the endpoint. e.g. username=johndoe@example,password=password123
    """
    return ResponseSchema(detail="tokens retrieval successful", data=tokens)
