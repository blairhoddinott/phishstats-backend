import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    songs: Mapped[list["AlbumSong"]] = relationship(
        back_populates="album", cascade="all, delete-orphan", order_by="AlbumSong.track_number"
    )


class AlbumSong(Base):
    __tablename__ = "album_songs"
    __table_args__ = (
        UniqueConstraint("album_id", "song_id", name="uq_album_song"),
        UniqueConstraint("album_id", "track_number", name="uq_album_track_number"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)
    song_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("songs.id", ondelete="CASCADE"), nullable=False)
    track_number: Mapped[int] = mapped_column(Integer, nullable=False)

    album: Mapped["Album"] = relationship(back_populates="songs")
    song: Mapped["Song"] = relationship(back_populates="albums")
