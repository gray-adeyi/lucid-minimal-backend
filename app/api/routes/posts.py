from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request

from app import crud
from app.api.deps import AuthenticatedUserDep, SessionDep
from app.models import Post
from app.schema import CreatePostSchema, ResponseSchema, PostDetailSchema

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

MAX_POST_PAYLOAD_SIZE = 1_000_000


@posts_router.post("/")
async def create_post(
    request: Request,
    body: CreatePostSchema,
    session: SessionDep,
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
):
    content_length = int(request.headers.get("content_length", "0"))
    if content_length > MAX_POST_PAYLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="payload has exceeded the maximum of 1MB",
        )
    new_post = Post(text=body.text, author_id=user.id)
    await crud.create_post(session=session, data=new_post)
    return ResponseSchema(data=PostDetailSchema.from_db_model(new_post))


@posts_router.get("/")
async def get_posts(
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
):
    raise NotImplementedError("This endpoint is yet to  be implemented")


@posts_router.get("/{id}/")
async def get_post_detail(
    id: UUID,
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
):
    raise NotImplementedError("This endpoint is yet to  be implemented")


@posts_router.delete("/{id}/")
async def delete_post(
    id: UUID,
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
):
    raise NotImplementedError("This endpoint is yet to  be implemented")
