import pytest
from utils.coordinates import Coordinates


def test_create_coordinates():
    c = Coordinates()
    assert c.x == 0
    assert c.y == 0


def test_eq():
    c1 = Coordinates(3, 4)
    c2 = Coordinates(3, 4)
    assert c1 == c2
    assert (3, 4) == c1


def test_iter():
    c = Coordinates(3, 4)
    x, y = c
    assert x == 3
    assert y == 4


def test_distance():
    c1 = Coordinates(1, 1)
    c2 = Coordinates(4, 5)
    assert c1.distance(c2) == 5
    assert c2.distance(c1) == 5


def test_distance_invalid_input():
    c = Coordinates(3, 4)
    with pytest.raises(ValueError):
        c.distance(None)
    with pytest.raises(ValueError):
        c.distance("not a coordinate")
