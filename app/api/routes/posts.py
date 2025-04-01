from uuid import UUID

from fastapi import APIRouter

posts_router =  APIRouter(prefix="/posts",tags=["Posts"])

@posts_router.post('/')
async def create_post():
    ...
@posts_router.get('/')
async def get_posts():
    ...

@posts_router.get('/{id}/')
async def get_post_detail(id: UUID):
    ...

@posts_router.delete('/{id}/')
async def delete_post(id: UUID):
    ...
