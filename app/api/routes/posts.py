from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AuthenticatedUserDep

posts_router = APIRouter(prefix="/posts", tags=["Posts"])


@posts_router.post("/")
async def create_post(
    user: AuthenticatedUserDep,  # noqa: ARG001 ignore unused arg, it is used to protect route
):
    raise NotImplementedError("This endpoint is yet to  be implemented")


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
