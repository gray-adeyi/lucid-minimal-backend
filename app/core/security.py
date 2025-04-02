from passlib.context import CryptContext


def hash_password(password: str, password_context: CryptContext) -> str:
    """Converts the provided password into a hashed equivalent of the password.

    Args:
        password: The password to be hashed.
        password_context: Helper for hashing & verifying passwords using multiple algorithms.
    Returns:
        the hashed equivalent of the password
    """
    return password_context.hash(password)


def verify_password(
    password: str, hashed_password: str, password_context: CryptContext
) -> bool:
    """Verifies a password with its hash.

    Verifies the hash returned from hashing the `password` matches the `hashed_password`

    Args:
        password: The password to be verified.
        hashed_password: The expected valid hash of the `password`
        password_context: Helper for hashing & verifying passwords using multiple algorithms.

    Returns:
        ``True`` if the password is valid or otherwise.
    """
    return password_context.verify(password, hashed_password)
