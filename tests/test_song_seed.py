from scripts.albums_seed import ALBUMS
from scripts.songs_seed import ALBUM_SONGS, SONGS


def test_song_seed_count() -> None:
    assert len(SONGS) == 187


def test_song_seed_has_unique_names() -> None:
    names = [song["name"] for song in SONGS]
    assert len(names) == len(set(names))


def test_album_song_mapping_covers_seeded_albums_except_unmapped_placeholder() -> None:
    seeded_album_names = {album["name"] for album in ALBUMS}
    assert seeded_album_names - {"Get More Down"} == set(ALBUM_SONGS)


def test_album_song_tracks_reference_seeded_song_names() -> None:
    song_names = {song["name"] for song in SONGS}
    for album_name, tracks in ALBUM_SONGS.items():
        assert tracks, f"{album_name} should have at least one track"
        for track in tracks:
            assert track in song_names


def test_rift_retains_repeated_lengthwise_track() -> None:
    assert ALBUM_SONGS["Rift"].count("Lengthwise") == 2


def test_known_album_track_order_samples() -> None:
    assert ALBUM_SONGS["Junta"][:3] == ["Fee", "You Enjoy Myself", "Esther"]
    assert ALBUM_SONGS["Sigma Oasis"][-2:] == ["A Life Beyond The Dream", "Thread"]
    assert ALBUM_SONGS["Evolve"][-3:] == ["Valdese", "The Well", "Mercy"]
