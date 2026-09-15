from scripts.import_csv import normalize_producers


def test_normalize_producers():
    producers = normalize_producers(
        "Bob Cavallo, Joe Ruffalo and Steve Fargnoli"
    )

    assert producers == [
        "Bob Cavallo",
        "Joe Ruffalo",
        "Steve Fargnoli",
    ]

def test_normalize_single_producer():
    producers = normalize_producers("Allan Carr")

    assert producers == ["Allan Carr"]

def test_normalize_multiple_producers_with_comma():
    producers = normalize_producers(
        "Producer A, Producer B"
    )

    assert producers == [
        "Producer A",
        "Producer B",
    ]