from scripts.albums_seed import ALBUMS


def test_album_seed_count() -> None:
    assert len(ALBUMS) == 16


def test_album_seed_contains_known_titles() -> None:
    expected = {
        ("Junta", 1989),
        ("Lawn Boy", 1990),
        ("A Picture of Nectar", 1992),
        ("Rift", 1993),
        ("Hoist", 1994),
        ("Billy Breathes", 1996),
        ("The Story of the Ghost", 1998),
        ("Farmhouse", 2000),
        ("Round Room", 2002),
        ("Undermind", 2004),
        ("Joy", 2009),
        ("Fuego", 2014),
        ("Big Boat", 2016),
        ("Sigma Oasis", 2020),
        ("Get More Down", 2024),
        ("Evolve", 2024),
    }

    actual = {(album["name"], album["year"]) for album in ALBUMS}
    assert actual == expected
