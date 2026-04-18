"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-18 01:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "albums",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index(op.f("ix_albums_name"), "albums", ["name"], unique=False)
    op.create_index(op.f("ix_albums_year"), "albums", ["year"], unique=False)

    op.create_table(
        "songs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("first_played", sa.Date(), nullable=True),
        sa.Column("last_played", sa.Date(), nullable=True),
        sa.Column("times_played", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("name", name="uq_songs_name"),
    )
    op.create_index(op.f("ix_songs_name"), "songs", ["name"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email_address", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("email_address", name="uq_users_email_address"),
        sa.UniqueConstraint("slug", name="uq_users_slug"),
    )
    op.create_index(op.f("ix_users_email_address"), "users", ["email_address"], unique=False)
    op.create_index(op.f("ix_users_slug"), "users", ["slug"], unique=False)

    op.create_table(
        "concerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("concert_date", sa.Date(), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("state_province", sa.String(length=120), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=False),
        sa.Column("location_geopoint", Geography(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index(op.f("ix_concerts_concert_date"), "concerts", ["concert_date"], unique=False)

    op.create_table(
        "album_songs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("album_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("albums.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("track_number", sa.Integer(), nullable=False),
        sa.UniqueConstraint("album_id", "song_id", name="uq_album_song"),
        sa.UniqueConstraint("album_id", "track_number", name="uq_album_track_number"),
    )

    op.create_table(
        "chasing_lists",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_chasing_lists_user_id"),
    )

    op.create_table(
        "concert_attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("concert_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("user_id", "concert_id", name="uq_user_concert_attendance"),
    )

    op.create_table(
        "concert_setlist_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("concert_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("songs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.UniqueConstraint("concert_id", "position", name="uq_concert_setlist_position"),
    )

    op.create_table(
        "chasing_list_songs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("chasing_list_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chasing_lists.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.CheckConstraint("position >= 1 AND position <= 5", name="ck_chasing_list_position_range"),
        sa.UniqueConstraint("chasing_list_id", "song_id", name="uq_chasing_list_song"),
        sa.UniqueConstraint("chasing_list_id", "position", name="uq_chasing_list_position"),
    )


def downgrade() -> None:
    op.drop_table("chasing_list_songs")
    op.drop_table("concert_setlist_entries")
    op.drop_table("concert_attendance")
    op.drop_table("chasing_lists")
    op.drop_table("album_songs")
    op.drop_index(op.f("ix_concerts_concert_date"), table_name="concerts")
    op.drop_table("concerts")
    op.drop_index(op.f("ix_users_slug"), table_name="users")
    op.drop_index(op.f("ix_users_email_address"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_songs_name"), table_name="songs")
    op.drop_table("songs")
    op.drop_index(op.f("ix_albums_year"), table_name="albums")
    op.drop_index(op.f("ix_albums_name"), table_name="albums")
    op.drop_table("albums")
