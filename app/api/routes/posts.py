from uuid import UUID
from typing import Never, Annotated, cast
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from app import crud
from app.api.deps import AuthenticatedUserDep, SessionDep
from app.models import Post
from app.schema import CreatePostSchema, ResponseSchema, PostDetailSchema, PostSchema

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

MAX_POST_PAYLOAD_SIZE = 1_000_000  # 1 Mb in bytes
GET_POST_CACHE_DURATION = 5 * 60  # 5 minutes to seconds


async def get_post_by_id(
    id: UUID, user: AuthenticatedUserDep, session: SessionDep
) -> Post | Never:
    post = await crud.get_post_by_id(session=session, id=id)
    if not post or post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found",
        )
    return post


@posts_router.post("/", status_code=status.HTTP_201_CREATED)
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
    return ResponseSchema(
        data=PostDetailSchema.model_validate(new_post, from_attributes=True)
    )


@posts_router.get("/")
async def get_posts(
    session: SessionDep,
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
    response: Response,
):
    # Simple caching
    response.headers["Cache-Control"] = f"public, max-age={GET_POST_CACHE_DURATION}"
    posts = await crud.get_posts(session=session, author_id=user.id)
    posts = cast(
        list[PostSchema],
        [PostSchema.model_validate(post, from_attributes=True) for post in posts],
    )
    # Response is not paginated for simplicity
    return ResponseSchema(data=posts)


@posts_router.get("/{id}/")
async def get_post_detail(
    id: UUID,
    post: Annotated[Post, Depends(get_post_by_id)],
):
    return ResponseSchema(
        data=PostDetailSchema.model_validate(post, from_attributes=True)
    )


@posts_router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: UUID,
    session: SessionDep,
    post: Annotated[Post, Depends(get_post_by_id)],
):
    await crud.delete_post(session=session, post=post)
