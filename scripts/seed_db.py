"""Placeholder database seed script."""

from passlib.context import CryptContext
from slugify import slugify


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def main() -> None:
    password_hash = pwd_context.hash("ChangeMe123!")
    example_slug = slugify("Trey Anastasio")[:20]
    print("Seed placeholder")
    print({"example_user_slug": example_slug, "example_password_hash": password_hash})


if __name__ == "__main__":
    main()
