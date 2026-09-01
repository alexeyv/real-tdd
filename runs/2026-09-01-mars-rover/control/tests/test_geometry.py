"""Grid arithmetic: wrapping longitude, crossing poles, rejecting bad grids."""

import pytest

from rover import Heading, Planet, Position

NORTH_ROW = 5  # a 10x6 planet: row 5 is the north pole row, row 0 the south


@pytest.fixture
def planet() -> Planet:
    return Planet(width=10, height=6)


def test_east_off_the_last_column_wraps_to_zero(planet: Planet) -> None:
    assert planet.step(Position(9, 5), Heading.EAST) == (Position(0, 5), Heading.EAST)


def test_west_off_column_zero_wraps_to_the_last_column(planet: Planet) -> None:
    assert planet.step(Position(0, 3), Heading.WEST) == (Position(9, 3), Heading.WEST)


def test_ordinary_moves_change_latitude_without_touching_the_heading(
    planet: Planet,
) -> None:
    assert planet.step(Position(4, 2), Heading.NORTH) == (Position(4, 3), Heading.NORTH)
    assert planet.step(Position(4, 2), Heading.SOUTH) == (Position(4, 1), Heading.SOUTH)


def test_forward_off_the_north_pole_row_crosses_the_pole(planet: Planet) -> None:
    assert planet.step(Position(2, NORTH_ROW), Heading.NORTH) == (
        Position(7, NORTH_ROW),
        Heading.SOUTH,
    )


def test_forward_off_the_south_pole_row_crosses_the_pole(planet: Planet) -> None:
    assert planet.step(Position(2, 0), Heading.SOUTH) == (Position(7, 0), Heading.NORTH)


def test_backward_off_the_north_pole_row_crosses_the_pole(planet: Planet) -> None:
    assert planet.step(Position(2, NORTH_ROW), Heading.SOUTH, forward=False) == (
        Position(7, NORTH_ROW),
        Heading.NORTH,
    )


def test_backward_off_the_south_pole_row_crosses_the_pole(planet: Planet) -> None:
    assert planet.step(Position(2, 0), Heading.NORTH, forward=False) == (
        Position(7, 0),
        Heading.SOUTH,
    )


def test_backward_away_from_a_pole_does_not_cross(planet: Planet) -> None:
    assert planet.step(Position(2, NORTH_ROW), Heading.NORTH, forward=False) == (
        Position(2, NORTH_ROW - 1),
        Heading.NORTH,
    )


@pytest.mark.parametrize("x", range(10))
def test_crossing_a_pole_twice_returns_to_the_start(planet: Planet, x: int) -> None:
    position, heading = planet.step(Position(x, NORTH_ROW), Heading.NORTH)
    back = planet.step(position, heading, forward=False)
    assert back == (Position(x, NORTH_ROW), Heading.NORTH)


def test_on_the_narrowest_planet_the_antipode_is_the_next_column() -> None:
    planet = Planet(width=2, height=3)
    assert planet.step(Position(0, 2), Heading.NORTH) == (Position(1, 2), Heading.SOUTH)
    assert planet.step(Position(1, 2), Heading.NORTH) == (Position(0, 2), Heading.SOUTH)


def test_a_one_row_planet_is_all_pole() -> None:
    planet = Planet(width=4, height=1)
    assert planet.step(Position(1, 0), Heading.NORTH) == (Position(3, 0), Heading.SOUTH)
    assert planet.step(Position(1, 0), Heading.SOUTH) == (Position(3, 0), Heading.NORTH)


def test_turning_cycles_through_the_compass() -> None:
    assert Heading.NORTH.right() == Heading.EAST
    assert Heading.EAST.right() == Heading.SOUTH
    assert Heading.SOUTH.right() == Heading.WEST
    assert Heading.WEST.right() == Heading.NORTH

    assert Heading.NORTH.left() == Heading.WEST
    assert Heading.WEST.left() == Heading.SOUTH

    assert Heading.NORTH.opposite() == Heading.SOUTH
    assert Heading.EAST.opposite() == Heading.WEST


def test_obstacles_are_reported_by_square(planet: Planet) -> None:
    mapped = Planet(width=10, height=6, obstacles=[(1, 1), (3, 4)])
    assert mapped.has_obstacle(Position(1, 1))
    assert mapped.has_obstacle(Position(3, 4))
    assert not mapped.has_obstacle(Position(2, 1))
    assert not planet.has_obstacle(Position(1, 1))


def test_an_odd_width_has_no_antipode() -> None:
    with pytest.raises(ValueError):
        Planet(width=9, height=6)


@pytest.mark.parametrize("size", [(0, 6), (10, 0), (-2, 6), (10, -1)])
def test_a_grid_needs_positive_dimensions(size: tuple[int, int]) -> None:
    with pytest.raises(ValueError):
        Planet(width=size[0], height=size[1])


@pytest.mark.parametrize("square", [(5, 7), (5, -1), (12, 3), (-1, 3)])
def test_obstacles_must_be_on_the_grid(square: tuple[int, int]) -> None:
    with pytest.raises(ValueError):
        Planet(width=10, height=6, obstacles=[square])


def test_a_square_listed_twice_is_one_obstacle() -> None:
    planet = Planet(width=10, height=6, obstacles=[(1, 1), (1, 1), (3, 4)])
    assert planet.obstacles == frozenset({Position(1, 1), Position(3, 4)})


def test_obstacles_survive_being_given_as_a_one_shot_iterator() -> None:
    squares = iter([(1, 1), (3, 4)])  # a generator is drained by the first read
    planet = Planet(width=10, height=6, obstacles=squares)
    assert planet.has_obstacle(Position(1, 1))
    assert planet.has_obstacle(Position(1, 1))
    assert planet.has_obstacle(Position(3, 4))


def test_a_heading_letter_is_read_with_surrounding_space_and_any_case() -> None:
    assert Heading.parse(" n ") is Heading.NORTH
    assert Heading.parse("\tE\n") is Heading.EAST
