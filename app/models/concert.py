import uuid
from datetime import date, datetime

from geoalchemy2 import Geography
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Concert(Base):
    __tablename__ = "concerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concert_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state_province: Mapped[str | None] = mapped_column(String(120), nullable=True)
    country: Mapped[str] = mapped_column(String(120), nullable=False)
    location_geopoint = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    setlist_entries: Mapped[list["ConcertSetlistEntry"]] = relationship(
        back_populates="concert", cascade="all, delete-orphan", order_by="ConcertSetlistEntry.position"
    )
    attendees: Mapped[list["ConcertAttendance"]] = relationship(back_populates="concert", cascade="all, delete-orphan")


class ConcertSetlistEntry(Base):
    __tablename__ = "concert_setlist_entries"
    __table_args__ = (
        UniqueConstraint("concert_id", "position", name="uq_concert_setlist_position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False)
    song_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("songs.id", ondelete="RESTRICT"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    concert: Mapped["Concert"] = relationship(back_populates="setlist_entries")
    song: Mapped["Song"] = relationship(back_populates="setlists")


class ConcertAttendance(Base):
    __tablename__ = "concert_attendance"
    __table_args__ = (
        UniqueConstraint("user_id", "concert_id", name="uq_user_concert_attendance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="concerts_attended")
    concert: Mapped["Concert"] = relationship(back_populates="attendees")
