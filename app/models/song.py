import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("albums.id", ondelete="SET NULL"), nullable=True, index=True)
    track_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    first_played: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_played: Mapped[date | None] = mapped_column(Date, nullable=True)
    times_played: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    album: Mapped["Album | None"] = relationship(back_populates="songs")
    setlists: Mapped[list["ConcertSetlistEntry"]] = relationship(back_populates="song")
    chasing_entries: Mapped[list["ChasingListSong"]] = relationship(back_populates="song")
