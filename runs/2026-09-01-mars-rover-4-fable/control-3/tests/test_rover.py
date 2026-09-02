import pytest

from mars_rover import Heading, Outcome, Planet, Report, Rover


def make_rover(position=(0, 0), heading=Heading.N, obstacles=(), discovered=()):
    planet = Planet(4, 3, obstacles=set(obstacles) | set(discovered))
    rover = Rover(planet, position, heading)
    for obstacle in discovered:
        rover._discovered.append(obstacle)
    return rover


def assert_report_matches_rover(report, rover):
    assert report.position == rover.position
    assert report.heading == rover.heading


def test_basic_moves():
    rover = make_rover()
    report = rover.execute("FFRFF")
    assert report == Report((2, 2), Heading.E, Outcome.COMPLETED)
    assert_report_matches_rover(report, rover)


def test_backward():
    rover = make_rover((0, 1), Heading.N)
    assert rover.execute("B") == Report((0, 0), Heading.N, Outcome.COMPLETED)


def test_longitude_wrap():
    rover = make_rover()
    assert rover.execute("RB") == Report((3, 0), Heading.E, Outcome.COMPLETED)


def test_north_pole_cross():
    rover = make_rover((0, 2), Heading.N)
    assert rover.execute("F") == Report((2, 2), Heading.S, Outcome.COMPLETED)


def test_south_pole_cross():
    rover = make_rover((1, 0), Heading.S)
    assert rover.execute("F") == Report((3, 0), Heading.N, Outcome.COMPLETED)


def test_backward_over_pole():
    rover = make_rover((0, 2), Heading.S)
    assert rover.execute("B") == Report((2, 2), Heading.N, Outcome.COMPLETED)


def test_unknown_obstacle_blocks_and_is_learned():
    rover = make_rover(obstacles=[(0, 2)])
    report = rover.execute("FFRF")
    assert report == Report((0, 1), Heading.N, Outcome.BLOCKED, (0, 2))
    assert_report_matches_rover(report, rover)
    assert rover.discovered_obstacles == ((0, 2),)


def test_known_obstacle_refused():
    rover = make_rover(discovered=[(0, 2)])
    report = rover.execute("FF")
    assert report == Report((0, 0), Heading.N, Outcome.REFUSED, (0, 2))
    assert_report_matches_rover(report, rover)
    assert rover.discovered_obstacles == ((0, 2),)


def test_refusal_after_a_turn():
    rover = make_rover((0, 1), Heading.E, discovered=[(0, 2)])
    report = rover.execute("LF")
    assert report == Report((0, 1), Heading.E, Outcome.REFUSED, (0, 2))
    assert rover.heading is Heading.E
    assert rover.position == (0, 1)


def test_turn_only_near_known_obstacle():
    rover = make_rover((0, 1), Heading.N, discovered=[(0, 2)])
    assert rover.execute("LR") == Report((0, 1), Heading.N, Outcome.COMPLETED)


def test_repeated_bump_records_once():
    rover = make_rover((0, 1), Heading.N, obstacles=[(0, 2)])
    assert rover.execute("F").outcome is Outcome.BLOCKED
    assert rover.discovered_obstacles == ((0, 2),)
    # Now known: the same string is refused, not bumped again.
    assert rover.execute("F").outcome is Outcome.REFUSED
    assert rover.discovered_obstacles == ((0, 2),)


def test_known_obstacle_refused_from_another_direction():
    rover = make_rover((0, 1), Heading.N, obstacles=[(0, 2)])
    rover.execute("F")  # bump from below
    rover.execute("RFL")  # to (1, 1) heading N; refusal-free path
    assert rover.position == (1, 1)
    # Approach (0, 2) from (1, 2) heading W: prediction knows it, refuses.
    report = rover.execute("FLF")
    assert report.outcome is Outcome.REFUSED
    assert rover.discovered_obstacles == ((0, 2),)


def test_obstacle_across_pole_blocks_whole_step():
    rover = make_rover((0, 2), Heading.N, obstacles=[(2, 2)])
    report = rover.execute("F")
    assert report == Report((0, 2), Heading.N, Outcome.BLOCKED, (2, 2))
    assert rover.discovered_obstacles == ((2, 2),)


def test_blocked_after_turn_keeps_turned_heading():
    rover = make_rover((1, 0), Heading.N, obstacles=[(2, 0)])
    report = rover.execute("RF")
    assert report == Report((1, 0), Heading.E, Outcome.BLOCKED, (2, 0))
    assert rover.heading is Heading.E


def test_blocked_backward_keeps_heading():
    rover = make_rover((0, 1), Heading.N, obstacles=[(0, 0)])
    assert rover.execute("B") == Report((0, 1), Heading.N, Outcome.BLOCKED, (0, 0))


def test_blocked_after_pole_crossing_keeps_flipped_heading():
    rover = make_rover((0, 2), Heading.N, obstacles=[(2, 1)])
    assert rover.execute("FF") == Report((2, 2), Heading.S, Outcome.BLOCKED, (2, 1))


def test_backward_refused_by_known_obstacle():
    rover = make_rover((0, 1), Heading.N, discovered=[(0, 0)])
    report = rover.execute("B")
    assert report == Report((0, 1), Heading.N, Outcome.REFUSED, (0, 0))
    assert_report_matches_rover(report, rover)


def test_known_obstacle_across_pole_refused():
    rover = make_rover((0, 2), Heading.N, discovered=[(2, 2)])
    report = rover.execute("F")
    assert report == Report((0, 2), Heading.N, Outcome.REFUSED, (2, 2))
    assert rover.position == (0, 2)
    assert rover.heading is Heading.N
    assert rover.discovered_obstacles == ((2, 2),)


def test_discovery_order():
    rover = make_rover((1, 0), Heading.N, obstacles=[(1, 1), (2, 0)])
    rover.execute("F")  # bumps A = (1, 1)
    rover.execute("RF")  # bumps B = (2, 0)
    assert rover.discovered_obstacles == ((1, 1), (2, 0))


def test_prediction_uses_only_discovered_obstacles():
    # Unknown at step 1, known at step 2: refused, unknown stays undiscovered.
    rover = make_rover(obstacles=[(0, 1)], discovered=[(0, 2)])
    report = rover.execute("FF")
    assert report == Report((0, 0), Heading.N, Outcome.REFUSED, (0, 2))
    assert rover.discovered_obstacles == ((0, 2),)


def test_bad_command_raises_and_nothing_moves():
    rover = make_rover()
    with pytest.raises(ValueError):
        rover.execute("FX")
    assert rover.position == (0, 0)
    assert rover.heading is Heading.N
    assert rover.discovered_obstacles == ()


@pytest.mark.parametrize("position", [(7, 5), (4, 0), (0, 3), (-1, 0)])
def test_off_grid_start_rejected(position):
    with pytest.raises(ValueError):
        Rover(Planet(4, 3), position, Heading.N)


def test_start_on_obstacle_rejected():
    with pytest.raises(ValueError):
        Rover(Planet(4, 3, obstacles=[(0, 0)]), (0, 0), Heading.N)


def test_empty_command_string_completes():
    rover = make_rover()
    assert rover.execute("") == Report((0, 0), Heading.N, Outcome.COMPLETED)


def test_discovered_obstacles_is_a_snapshot():
    rover = make_rover(obstacles=[(0, 1)])
    snapshot = rover.discovered_obstacles
    rover.execute("F")
    assert snapshot == ()
    assert rover.discovered_obstacles == ((0, 1),)
