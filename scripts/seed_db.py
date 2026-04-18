"""Database seed script for scaffold data."""

from __future__ import annotations

import asyncio
from collections.abc import Iterable

from passlib.context import CryptContext
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Album
from scripts.albums_seed import ALBUMS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_albums() -> int:
    seeded = 0
    async with AsyncSessionLocal() as session:
        for album in ALBUMS:
            existing = await session.scalar(select(Album).where(Album.name == album["name"]))
            if existing:
                continue
            session.add(Album(name=album["name"], year=album["year"]))
            seeded += 1

        await session.commit()
    return seeded


def preview_seed_payload() -> dict[str, object]:
    password_hash = pwd_context.hash("ChangeMe123!")
    return {
        "albums": list(ALBUMS),
        "album_count": len(ALBUMS),
        "example_password_hash": password_hash,
    }


def print_album_summary(albums: Iterable[dict[str, int | str]]) -> None:
    for album in albums:
        print(f"- {album['name']} ({album['year']})")


async def main() -> None:
    seeded = await seed_albums()
    payload = preview_seed_payload()
    print(f"Inserted {seeded} new albums.")
    print_album_summary(payload["albums"])


if __name__ == "__main__":
    asyncio.run(main())
