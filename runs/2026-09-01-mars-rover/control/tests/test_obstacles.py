"""Bumping into an obstacle the rover has never met."""

import pytest

from rover import Heading, Outcome, Planet, Position, Rover

OBSTACLE = Position(5, 7)


@pytest.fixture
def planet() -> Planet:
    return Planet(width=10, height=10, obstacles=[OBSTACLE])


def test_a_bump_stops_the_rover_short_of_the_obstacle(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    report = rover.execute("FFF")
    assert report.position == Position(5, 6)
    assert report.outcome is Outcome.BLOCKED
    assert report.obstacle == OBSTACLE
    assert report.stopped


def test_the_rest_of_the_string_is_abandoned(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    rover.execute("FFRF")
    # The third command would have turned east; it never ran.
    assert (rover.position, rover.heading) == (Position(5, 6), Heading.NORTH)


def test_a_blocked_move_leaves_the_heading_alone_at_a_pole() -> None:
    planet = Planet(width=10, height=10, obstacles=[(5, 9)])
    rover = Rover(planet, (0, 9), Heading.NORTH)
    report = rover.execute("F")
    # Crossing would land on (5, 9) facing south; the bump cancels both.
    assert (report.position, report.heading) == (Position(0, 9), Heading.NORTH)
    assert report.obstacle == Position(5, 9)


def test_a_backward_move_can_bump(planet: Planet) -> None:
    rover = Rover(planet, (5, 6), Heading.SOUTH)
    report = rover.execute("B")
    assert (report.position, report.heading) == (Position(5, 6), Heading.SOUTH)
    assert report.outcome is Outcome.BLOCKED
    assert report.obstacle == OBSTACLE


def test_a_clear_path_past_an_obstacle_completes(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    report = rover.execute("FRFLFF")
    assert report.outcome is Outcome.COMPLETED
    assert report.obstacle is None
    assert (report.position, report.heading) == (Position(6, 8), Heading.NORTH)
    assert rover.discovered_obstacles == ()


def test_turning_never_bumps(planet: Planet) -> None:
    rover = Rover(planet, (5, 6), Heading.NORTH)
    report = rover.execute("LRRL")
    assert report.outcome is Outcome.COMPLETED
    assert (report.position, report.heading) == (Position(5, 6), Heading.NORTH)
