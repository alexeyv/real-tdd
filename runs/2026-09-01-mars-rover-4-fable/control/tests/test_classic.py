"""The classic part: movement, turning, longitude wrap, unknown obstacles."""

import pytest

from mars_rover import Planet, Report, Rover


def rover(x=0, y=0, heading="N", width=10, height=10, obstacles=()):
    return Rover(Planet(width, height, obstacles), x, y, heading)


def test_starts_where_and_how_it_was_created():
    r = rover(3, 4, "E")
    assert r.position == (3, 4)
    assert r.heading == "E"


@pytest.mark.parametrize(
    "heading, expected",
    [("N", (5, 6)), ("E", (6, 5)), ("S", (5, 4)), ("W", (4, 5))],
)
def test_forward_moves_one_square_in_heading(heading, expected):
    assert rover(5, 5, heading).execute("F").position == expected


@pytest.mark.parametrize(
    "heading, expected",
    [("N", (5, 4)), ("E", (4, 5)), ("S", (5, 6)), ("W", (6, 5))],
)
def test_backward_moves_one_square_against_heading(heading, expected):
    assert rover(5, 5, heading).execute("B").position == expected


@pytest.mark.parametrize("commands, expected", [("L", "W"), ("LL", "S"), ("LLL", "E"), ("LLLL", "N")])
def test_left_turns_counterclockwise(commands, expected):
    r = rover(heading="N")
    assert r.execute(commands).heading == expected
    assert r.position == (0, 0)


@pytest.mark.parametrize("commands, expected", [("R", "E"), ("RR", "S"), ("RRR", "W"), ("RRRR", "N")])
def test_right_turns_clockwise(commands, expected):
    assert rover(heading="N").execute(commands).heading == expected


def test_commands_run_in_order():
    report = rover(2, 2, "N").execute("FFRFFLB")
    assert report == Report(position=(4, 3), heading="N")


def test_empty_command_string_changes_nothing():
    report = rover(2, 2, "N").execute("")
    assert report == Report(position=(2, 2), heading="N")
    assert not report.stopped_by_obstacle


def test_longitude_wraps_east_and_west():
    assert rover(9, 5, "E").execute("F").position == (0, 5)
    assert rover(0, 5, "W").execute("F").position == (9, 5)
    assert rover(0, 5, "E").execute("B").position == (9, 5)


def test_unknown_obstacle_stops_rover_and_abandons_rest_of_commands():
    r = rover(0, 0, "N", obstacles=[(0, 2)])
    report = r.execute("FFFRF")
    assert report.position == (0, 1)
    assert report.heading == "N"
    assert report.stopped_by_obstacle
    assert report.blocked_by == (0, 2)
    assert not report.refused
    assert r.position == (0, 1)


def test_turning_next_to_an_obstacle_never_hits_it():
    r = rover(0, 0, "N", obstacles=[(0, 1), (1, 0)])
    report = r.execute("LRLRRLLR")
    assert not report.stopped_by_obstacle
    assert report.position == (0, 0)


def test_report_after_clean_run_has_no_obstacle():
    report = rover(0, 0, "N", obstacles=[(5, 5)]).execute("FF")
    assert report.blocked_by is None
    assert not report.stopped_by_obstacle
    assert not report.refused


@pytest.mark.parametrize("commands", ["FXF", "ff", "F F", "F\n"])
def test_rejects_unknown_commands_without_moving(commands):
    r = rover(1, 1, "N")
    with pytest.raises(ValueError, match="unknown command"):
        r.execute(commands)
    assert r.position == (1, 1)


@pytest.mark.parametrize(
    "width, height, obstacles, message",
    [
        (5, 5, (), "width must be even"),
        (0, 5, (), "positive size"),
        (4, -1, (), "positive size"),
        (4, 4, [(4, 0)], "outside the 4x4 planet"),
        (4, 4, [(0, 4)], "outside the 4x4 planet"),
        (4, 4, [(1, 2, 3)], r"must be an \(x, y\) pair"),
    ],
)
def test_rejects_invalid_planets(width, height, obstacles, message):
    with pytest.raises(ValueError, match=message):
        Planet(width, height, obstacles)


@pytest.mark.parametrize(
    "x, y, heading, message",
    [(4, 0, "N", "outside the 4x4 planet"), (0, -1, "N", "outside"), (0, 0, "Q", "heading must be one of")],
)
def test_rejects_invalid_rovers(x, y, heading, message):
    with pytest.raises(ValueError, match=message):
        Rover(Planet(4, 4), x, y, heading)


def test_planet_obstacles_accept_any_iterable_of_pairs():
    planet = Planet(4, 4, obstacles=iter([[1, 1], (2, 2)]))
    assert planet.obstacles == frozenset({(1, 1), (2, 2)})
    assert planet.has_obstacle((1, 1))


def test_rover_repr_shows_state():
    r = rover(0, 0, "N", obstacles=[(0, 1)])
    r.execute("F")
    assert repr(r) == "Rover(position=(0, 0), heading='N', discovered_obstacles=[(0, 1)])"
