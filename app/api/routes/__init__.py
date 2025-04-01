from .auth import auth_router  # noqa: F401
from .posts import posts_router  # noqa: F401


__all__ = ["auth_router", "posts_router"]
