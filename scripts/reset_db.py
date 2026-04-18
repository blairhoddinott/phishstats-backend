"""Reset the scaffold database and reseed albums."""

from __future__ import annotations

import asyncio

from sqlalchemy import delete

from app.database import AsyncSessionLocal
from app.models import Album
from scripts.seed_db import seed_albums


async def reset_albums() -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Album))
        await session.commit()

    seeded = await seed_albums()
    print(f"Reset complete. Seeded {seeded} albums.")


if __name__ == "__main__":
    asyncio.run(reset_albums())
