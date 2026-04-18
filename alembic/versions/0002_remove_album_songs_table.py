"""remove album_songs table and move relationship onto songs

Revision ID: 0002_remove_album_songs_table
Revises: 0001_initial_schema
Create Date: 2026-04-18 14:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002_remove_album_songs_table"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("songs", sa.Column("album_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("songs", sa.Column("track_number", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_songs_album_id"), "songs", ["album_id"], unique=False)
    op.create_foreign_key("fk_songs_album_id_albums", "songs", "albums", ["album_id"], ["id"], ondelete="SET NULL")

    op.execute(
        """
        UPDATE songs
        SET album_id = album_songs.album_id,
            track_number = album_songs.track_number
        FROM album_songs
        WHERE songs.id = album_songs.song_id
        """
    )

    op.drop_table("album_songs")


def downgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    op.create_table(
        "album_songs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("album_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("albums.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("track_number", sa.Integer(), nullable=False),
        sa.UniqueConstraint("album_id", "song_id", name="uq_album_song"),
        sa.UniqueConstraint("album_id", "track_number", name="uq_album_track_number"),
    )

    op.execute(
        """
        INSERT INTO album_songs (id, album_id, song_id, track_number)
        SELECT uuid_generate_v4(), album_id, id, track_number
        FROM songs
        WHERE album_id IS NOT NULL AND track_number IS NOT NULL
        """
    )

    op.drop_constraint("fk_songs_album_id_albums", "songs", type_="foreignkey")
    op.drop_index(op.f("ix_songs_album_id"), table_name="songs")
    op.drop_column("songs", "track_number")
    op.drop_column("songs", "album_id")
