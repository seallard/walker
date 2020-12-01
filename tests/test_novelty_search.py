from novelty_search.novelty_search import Archive


def test_single_point_novelty_score():
    archive = Archive()
    archive.add_point((0,0))

    novelty_score = archive.get_novelty_score((1,0))

    assert novelty_score == 1


def test_existing_single_point_novelty_score():
    archive = Archive()
    archive.add_point((0,0))
    novelty_score = archive.get_novelty_score((0,0))

    assert novelty_score == 0


def test_multiple_novelty_score():
    archive = Archive()
    archive.add_point((0,0))
    archive.add_point((1,1))

    novelty_score = archive.get_novelty_score((2,2))

    assert novelty_score == (8**0.5 + 2**0.5)/2
