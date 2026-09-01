"""What the rover remembers, and how it behaves once it knows."""

import pytest

from rover import Heading, Outcome, Planet, Position, Rover

OBSTACLE = Position(5, 7)
OTHER = Position(3, 5)


@pytest.fixture
def planet() -> Planet:
    return Planet(width=10, height=10, obstacles=[OBSTACLE, OTHER])


def bump(rover: Rover) -> None:
    """Drive a rover standing at (5, 5) and facing north into ``OBSTACLE``.

    Leaves it at (5, 6), still facing north, with ``OBSTACLE`` discovered.
    """
    rover.execute("FFF")


def test_a_bump_is_recorded(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    assert rover.discovered_obstacles == (OBSTACLE,)


def test_meeting_the_same_obstacle_again_does_not_record_it_twice(
    planet: Planet,
) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    rover.execute("BB")  # back off and drive at it a second time
    second = rover.execute("FFF")
    # Known now, so the second run is refused rather than bumped -- either way
    # the obstacle is listed once.
    assert second.obstacle == OBSTACLE
    assert rover.discovered_obstacles == (OBSTACLE,)


def test_learning_the_same_obstacle_again_is_a_no_op(planet: Planet) -> None:
    """The dedup guard itself, reached directly.

    Once an obstacle is known the pre-flight refuses before the rover can
    touch it again, so no command string can drive a second bump. The rule
    only lives in the recording step, so that is where it is pinned.
    """
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)

    rover._learn(OBSTACLE)
    rover._learn(OBSTACLE)
    assert rover.discovered_obstacles == (OBSTACLE,)

    rover._learn(OTHER)
    rover._learn(OBSTACLE)
    assert rover.discovered_obstacles == (OBSTACLE, OTHER)


def test_obstacles_come_back_in_discovery_order(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    assert rover.discovered_obstacles == (OBSTACLE,)

    rover.execute("LLF")  # turn about, walk back down to (5, 5)
    rover.execute("RF")  # face west and take the first step, to (4, 5)
    rover.execute("F")  # and the second, into OTHER
    assert rover.discovered_obstacles == (OBSTACLE, OTHER)


def test_an_undiscovered_obstacle_is_not_known_in_advance(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    report = rover.execute("FFF")
    assert report.outcome is Outcome.BLOCKED  # not refused: it had no map


def test_a_string_that_would_hit_a_known_obstacle_is_refused(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    rover.execute("BB")
    assert rover.position == Position(5, 4)

    report = rover.execute("FFF")
    assert report.outcome is Outcome.REFUSED
    assert report.stopped
    assert report.obstacle == OBSTACLE
    assert (report.position, report.heading) == (Position(5, 4), Heading.NORTH)
    assert (rover.position, rover.heading) == (Position(5, 4), Heading.NORTH)


def test_refusal_swallows_the_turns_too(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    rover.execute("B")
    assert rover.position == Position(5, 5)

    report = rover.execute("RLFF")
    assert report.outcome is Outcome.REFUSED
    assert report.obstacle == OBSTACLE
    assert (rover.position, rover.heading) == (Position(5, 5), Heading.NORTH)


def test_a_refused_turn_does_not_survive(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)
    rover.execute("B")
    rover.execute("R")  # face east, so the refused L below would be visible
    assert rover.heading == Heading.EAST

    report = rover.execute("LFF")
    assert report.outcome is Outcome.REFUSED
    assert (rover.position, rover.heading) == (Position(5, 5), Heading.EAST)


def test_a_turn_only_string_is_never_refused(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)

    report = rover.execute("RL")
    assert report.outcome is Outcome.COMPLETED
    assert (rover.position, rover.heading) == (Position(5, 6), Heading.NORTH)


def test_a_route_around_a_known_obstacle_still_runs(planet: Planet) -> None:
    rover = Rover(planet, (5, 5), Heading.NORTH)
    bump(rover)

    report = rover.execute("RFLFF")
    assert report.outcome is Outcome.COMPLETED
    assert (report.position, report.heading) == (Position(6, 8), Heading.NORTH)


def test_the_look_ahead_follows_the_rover_across_a_pole() -> None:
    beyond = Position(5, 8)  # one square south of the antipode of (0, 9)
    planet = Planet(width=10, height=10, obstacles=[beyond])

    rover = Rover(planet, (0, 9), Heading.NORTH)
    report = rover.execute("FF")  # cross the pole, then walk into it
    assert report.outcome is Outcome.BLOCKED
    assert (rover.position, rover.heading) == (Position(5, 9), Heading.SOUTH)
    assert rover.discovered_obstacles == (beyond,)

    rover.execute("B")  # back over the pole to where it started
    assert (rover.position, rover.heading) == (Position(0, 9), Heading.NORTH)

    again = rover.execute("FF")  # the same route, now foreseen
    assert again.outcome is Outcome.REFUSED
    assert again.obstacle == beyond
    assert (rover.position, rover.heading) == (Position(0, 9), Heading.NORTH)


def test_discovery_is_per_rover(planet: Planet) -> None:
    veteran = Rover(planet, (5, 5), Heading.NORTH)
    bump(veteran)

    rookie = Rover(planet, (5, 5), Heading.NORTH)
    assert rookie.discovered_obstacles == ()
    assert rookie.execute("FFF").outcome is Outcome.BLOCKED
