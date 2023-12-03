from aoc2023 import d1a, d1b, d2a, d2b, d3a, d3b


def test_all():
    assert d1a.main() == 56397
    assert d1b.main() == 55701
    assert d2a.main() == 2505
    assert d2b.main() == 70265
    assert d3a.main() == 536202
    assert d3b.main() == 78272573
