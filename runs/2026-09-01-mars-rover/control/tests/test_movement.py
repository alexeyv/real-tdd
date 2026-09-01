"""Driving an empty planet: turning, command strings, and bad input."""

import pytest

from rover import Heading, Outcome, Planet, Position, Rover

NORTH_ROW = 5  # a 10x6 planet


@pytest.fixture
def planet() -> Planet:
    return Planet(width=10, height=6)


def test_a_fresh_rover_reports_where_it_was_put(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.WEST)
    assert rover.position == Position(3, 2)
    assert rover.heading == Heading.WEST
    assert rover.discovered_obstacles == ()


def test_a_heading_can_be_given_as_a_letter(planet: Planet) -> None:
    assert Rover(planet, (3, 2), "e").heading == Heading.EAST


def test_an_unknown_heading_letter_is_rejected(planet: Planet) -> None:
    with pytest.raises(ValueError):
        Rover(planet, (3, 2), "up")


def test_a_start_off_the_grid_is_rejected(planet: Planet) -> None:
    with pytest.raises(ValueError):
        Rover(planet, (10, 2), Heading.NORTH)
    with pytest.raises(ValueError):
        Rover(planet, (3, -1), Heading.NORTH)


def test_turning_changes_the_heading_and_nothing_else(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    report = rover.execute("RR")
    assert (report.position, report.heading) == (Position(3, 2), Heading.SOUTH)
    assert report.outcome is Outcome.COMPLETED
    assert report.obstacle is None
    assert not report.stopped


def test_an_empty_string_does_nothing(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    report = rover.execute("")
    assert (report.position, report.heading) == (Position(3, 2), Heading.NORTH)
    assert report.outcome is Outcome.COMPLETED


def test_forward_and_backward_along_a_row(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.EAST)
    rover.execute("FF")
    assert rover.position == Position(5, 2)
    rover.execute("B")
    assert (rover.position, rover.heading) == (Position(4, 2), Heading.EAST)


def test_moving_east_off_the_last_column_wraps(planet: Planet) -> None:
    rover = Rover(planet, (9, 5), Heading.EAST)
    report = rover.execute("F")
    assert (report.position, report.heading) == (Position(0, 5), Heading.EAST)


def test_a_command_string_runs_in_order(planet: Planet) -> None:
    rover = Rover(planet, (0, 0), Heading.NORTH)
    report = rover.execute("FFRFF")
    assert (report.position, report.heading) == (Position(2, 2), Heading.EAST)


def test_commands_are_case_insensitive(planet: Planet) -> None:
    rover = Rover(planet, (0, 0), Heading.NORTH)
    report = rover.execute("ffrff")
    assert (report.position, report.heading) == (Position(2, 2), Heading.EAST)


def test_forward_off_the_north_pole_row_crosses_the_pole(planet: Planet) -> None:
    rover = Rover(planet, (2, NORTH_ROW), Heading.NORTH)
    report = rover.execute("F")
    assert (report.position, report.heading) == (Position(7, NORTH_ROW), Heading.SOUTH)


def test_backward_off_the_north_pole_row_crosses_the_pole(planet: Planet) -> None:
    rover = Rover(planet, (2, NORTH_ROW), Heading.SOUTH)
    report = rover.execute("B")
    assert (report.position, report.heading) == (Position(7, NORTH_ROW), Heading.NORTH)


@pytest.mark.parametrize(
    "start, heading",
    [
        ((2, NORTH_ROW), Heading.NORTH),  # over the north pole and back
        ((2, 0), Heading.SOUTH),  # over the south pole and back
    ],
)
def test_a_pole_round_trip_is_a_no_op(
    planet: Planet, start: tuple[int, int], heading: Heading
) -> None:
    rover = Rover(planet, start, heading)

    rover.execute("F")  # the crossing itself, so a symmetric bug cannot hide
    assert (rover.position, rover.heading) == (
        Position((start[0] + 5) % 10, start[1]),
        heading.opposite(),
    )

    rover.execute("B")
    assert (rover.position, rover.heading) == (Position(*start), heading)


def test_one_string_can_cross_both_poles() -> None:
    planet = Planet(width=10, height=2)  # row 1 is north, row 0 is south
    rover = Rover(planet, (2, 1), Heading.NORTH)
    report = rover.execute("FFFF")  # right over the top, down, over the bottom, up
    assert (report.position, report.heading) == (Position(2, 1), Heading.NORTH)


def test_crossing_the_south_pole_from_row_zero(planet: Planet) -> None:
    rover = Rover(planet, (2, 0), Heading.SOUTH)
    report = rover.execute("F")
    assert (report.position, report.heading) == (Position(7, 0), Heading.NORTH)


def test_north_from_the_pole_row_is_not_a_wrap_to_the_far_row(planet: Planet) -> None:
    rover = Rover(planet, (2, NORTH_ROW), Heading.NORTH)
    rover.execute("F")
    assert rover.position.y == NORTH_ROW


def test_a_bad_command_character_is_rejected(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    with pytest.raises(ValueError):
        rover.execute("FX")


def test_a_ligature_is_not_two_commands(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    with pytest.raises(ValueError):
        rover.execute("\ufb00")  # the ff ligature: uppercases to "FF"
    assert rover.position == Position(3, 2)


def test_the_error_names_the_character_as_it_was_typed(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    with pytest.raises(ValueError, match="'x'"):
        rover.execute("fx")


def test_a_rejected_string_moves_nothing(planet: Planet) -> None:
    rover = Rover(planet, (3, 2), Heading.NORTH)
    with pytest.raises(ValueError):
        rover.execute("FX")
    assert (rover.position, rover.heading) == (Position(3, 2), Heading.NORTH)
