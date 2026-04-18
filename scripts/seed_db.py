"""Database seed script for scaffold data."""

from __future__ import annotations

import asyncio
from collections.abc import Iterable

from passlib.context import CryptContext
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Album, AlbumSong, Song
from scripts.albums_seed import ALBUMS
from scripts.songs_seed import ALBUM_SONGS, SONGS

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


async def seed_songs() -> int:
    seeded = 0
    async with AsyncSessionLocal() as session:
        for song in SONGS:
            existing = await session.scalar(select(Song).where(Song.name == song["name"]))
            if existing:
                continue
            session.add(Song(**song))
            seeded += 1

        await session.commit()
    return seeded


async def seed_album_songs() -> int:
    seeded = 0
    async with AsyncSessionLocal() as session:
        albums = {album.name: album for album in (await session.scalars(select(Album))).all()}
        songs = {song.name: song for song in (await session.scalars(select(Song))).all()}

        for album_name, track_names in ALBUM_SONGS.items():
            album = albums.get(album_name)
            if album is None:
                continue

            for track_number, song_name in enumerate(track_names, start=1):
                song = songs.get(song_name)
                if song is None:
                    continue

                existing = await session.scalar(
                    select(AlbumSong).where(
                        AlbumSong.album_id == album.id,
                        AlbumSong.track_number == track_number,
                    )
                )
                if existing:
                    continue

                session.add(AlbumSong(album_id=album.id, song_id=song.id, track_number=track_number))
                seeded += 1

        await session.commit()
    return seeded


def preview_seed_payload() -> dict[str, object]:
    password_hash = pwd_context.hash("ChangeMe123!")
    return {
        "albums": list(ALBUMS),
        "album_count": len(ALBUMS),
        "songs": list(SONGS),
        "song_count": len(SONGS),
        "album_song_count": sum(len(tracks) for tracks in ALBUM_SONGS.values()),
        "example_password_hash": password_hash,
    }


def print_album_summary(albums: Iterable[dict[str, int | str]]) -> None:
    for album in albums:
        print(f"- {album['name']} ({album['year']})")


async def main() -> None:
    seeded_albums = await seed_albums()
    seeded_songs = await seed_songs()
    seeded_album_songs = await seed_album_songs()
    payload = preview_seed_payload()
    print(f"Inserted {seeded_albums} new albums.")
    print(f"Inserted {seeded_songs} new songs.")
    print(f"Inserted {seeded_album_songs} new album-song links.")
    print_album_summary(payload["albums"])


if __name__ == "__main__":
    asyncio.run(main())
