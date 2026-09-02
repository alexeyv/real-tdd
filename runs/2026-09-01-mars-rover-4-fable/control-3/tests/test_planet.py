import pytest

from mars_rover import Heading, Planet


@pytest.fixture
def planet():
    return Planet(4, 3)


def test_step_north_moves_one_row(planet):
    assert planet.step((0, 0), Heading.N) == ((0, 1), Heading.N)


def test_longitude_wraps_west(planet):
    assert planet.step((0, 0), Heading.W) == ((3, 0), Heading.W)


def test_longitude_wraps_east(planet):
    assert planet.step((3, 0), Heading.E) == ((0, 0), Heading.E)


def test_north_pole_crossing(planet):
    assert planet.step((0, 2), Heading.N) == ((2, 2), Heading.S)


def test_south_pole_crossing(planet):
    assert planet.step((1, 0), Heading.S) == ((3, 0), Heading.N)


def test_latitude_never_wraps():
    planet = Planet(4, 3)
    position, _ = planet.step((0, 2), Heading.N)
    assert position[1] == 2
    position, _ = planet.step((0, 0), Heading.S)
    assert position[1] == 0


@pytest.mark.parametrize("width,height", [(5, 3), (0, 3), (4, 0), (-2, 3), (4, -1)])
def test_invalid_dimensions_rejected(width, height):
    with pytest.raises(ValueError):
        Planet(width, height)


@pytest.mark.parametrize("obstacle", [(9, 9), (4, 0), (0, 3), (-1, 0), (0, -1)])
def test_off_grid_obstacle_rejected(obstacle):
    with pytest.raises(ValueError):
        Planet(4, 3, obstacles=[obstacle])


def test_obstacles_stored_as_frozenset():
    planet = Planet(4, 3, obstacles=[(0, 2), (0, 2)])
    assert planet.obstacles == frozenset({(0, 2)})


@pytest.mark.parametrize(
    "heading,left,right,opposite",
    [
        (Heading.N, Heading.W, Heading.E, Heading.S),
        (Heading.E, Heading.N, Heading.S, Heading.W),
        (Heading.S, Heading.E, Heading.W, Heading.N),
        (Heading.W, Heading.S, Heading.N, Heading.E),
    ],
)
def test_heading_turns(heading, left, right, opposite):
    assert heading.turn_left() is left
    assert heading.turn_right() is right
    assert heading.opposite is opposite
