from uuid import UUID

from fastapi import APIRouter

posts_router = APIRouter(prefix="/posts", tags=["Posts"])


@posts_router.post("/")
async def create_post():
    raise NotImplementedError("This endpoint is yet to  be implemented")


@posts_router.get("/")
async def get_posts():
    raise NotImplementedError("This endpoint is yet to  be implemented")


@posts_router.get("/{id}/")
async def get_post_detail(id: UUID):
    raise NotImplementedError("This endpoint is yet to  be implemented")


@posts_router.delete("/{id}/")
async def delete_post(id: UUID):
    raise NotImplementedError("This endpoint is yet to  be implemented")
