# Database Overview

This backend uses PostgreSQL with the PostGIS extension enabled.

## Tables

### albums
- `id` UUID primary key
- `name` album name
- `year` release year
- seeded from `scripts/albums_seed.py` with the current Phish studio album catalogue

### songs
- `id` UUID primary key
- `name` song name
- `first_played` nullable date
- `last_played` nullable date
- `times_played` nullable integer
- seeded from `scripts/songs_seed.py` with the canonical studio album song catalogue

### album_songs
Join table between albums and songs.
- preserves track ordering via `track_number`
- seeded from `scripts/songs_seed.py` ordered per-album track mappings

### concerts
- `id` UUID primary key
- `concert_date`
- `city`
- `state_province`
- `country`
- `location_geopoint` PostGIS geography point

### concert_setlist_entries
Join table between concerts and songs.
- preserves setlist order via `position`

### users
- `id` UUID primary key
- `first_name`
- `last_name`
- `email_address`
- `password_hash`
- `slug` up to 20 characters

### concert_attendance
Join table between users and concerts attended.

### chasing_lists
One-to-one table linking a user to a chasing list.

### chasing_list_songs
Join table between chasing lists and songs.
- enforces positions 1 through 5
- unique song and position per chasing list

## Modeling notes
- The requested list relationships are implemented as association tables for ordering and referential integrity.
- The “max 5 songs” chasing list rule is enforced by the allowed positions `1..5` and should also be checked in application logic.
- `location_geopoint` uses PostGIS geography `POINT` with SRID 4326.
- The current seed path populates `albums`, `songs`, and `album_songs` from the studio discography data.
