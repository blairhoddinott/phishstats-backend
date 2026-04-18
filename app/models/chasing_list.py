import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.database import Base


class ChasingList(Base):
    __tablename__ = "chasing_lists"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="chasing_list")
    songs: Mapped[list["ChasingListSong"]] = relationship(
        back_populates="chasing_list", cascade="all, delete-orphan", order_by="ChasingListSong.position"
    )


class ChasingListSong(Base):
    __tablename__ = "chasing_list_songs"
    __table_args__ = (
        UniqueConstraint("chasing_list_id", "song_id", name="uq_chasing_list_song"),
        UniqueConstraint("chasing_list_id", "position", name="uq_chasing_list_position"),
        CheckConstraint("position >= 1 AND position <= 5", name="ck_chasing_list_position_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chasing_list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chasing_lists.id", ondelete="CASCADE"), nullable=False)
    song_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("songs.id", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    chasing_list: Mapped["ChasingList"] = relationship(back_populates="songs")
    song: Mapped["Song"] = relationship(back_populates="chasing_entries")

    @validates("position")
    def validate_position(self, _: str, value: int) -> int:
        if not 1 <= value <= 5:
            raise ValueError("Chasing list positions must be between 1 and 5")
        return value
