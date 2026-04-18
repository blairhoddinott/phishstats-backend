"""Seed verification helpers."""

from __future__ import annotations

import asyncio

from sqlalchemy import func, select

from app.database import AsyncSessionLocal
from app.models import Album
from scripts.albums_seed import ALBUMS


async def verify_albums() -> None:
    expected_names = {album["name"] for album in ALBUMS}

    async with AsyncSessionLocal() as session:
        count = await session.scalar(select(func.count(Album.id)))
        rows = await session.execute(select(Album.name, Album.year).order_by(Album.year, Album.name))

    albums = rows.all()
    seeded_names = {name for name, _ in albums}
    missing = sorted(expected_names - seeded_names)

    print(f"Album rows in database: {count}")
    if missing:
        print("Missing albums:")
        for name in missing:
            print(f"- {name}")
    else:
        print("All expected studio albums are present.")

    for name, year in albums:
        print(f"- {name} ({year})")


if __name__ == "__main__":
    asyncio.run(verify_albums())
