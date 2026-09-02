"""Twist 1: the grid maps a sphere, so pole rows are crossed, not wrapped."""

import pytest

from mars_rover import Planet, Rover

WIDTH, HEIGHT = 8, 5
NORTH_ROW, SOUTH_ROW = HEIGHT - 1, 0


def rover(x, y, heading, obstacles=()):
    return Rover(Planet(WIDTH, HEIGHT, obstacles), x, y, heading)


@pytest.mark.parametrize("x, far_x", [(0, 4), (3, 7), (4, 0), (7, 3)])
def test_forward_over_north_pole_lands_on_far_side_facing_south(x, far_x):
    report = rover(x, NORTH_ROW, "N").execute("F")
    assert report.position == (far_x, NORTH_ROW)
    assert report.heading == "S"


@pytest.mark.parametrize("x, far_x", [(0, 4), (3, 7), (4, 0), (7, 3)])
def test_forward_over_south_pole_lands_on_far_side_facing_north(x, far_x):
    report = rover(x, SOUTH_ROW, "S").execute("F")
    assert report.position == (far_x, SOUTH_ROW)
    assert report.heading == "N"


def test_backward_over_north_pole_matches_forward_in_opposite_heading():
    report = rover(1, NORTH_ROW, "S").execute("B")
    assert report.position == (5, NORTH_ROW)
    assert report.heading == "S"


def test_backward_over_south_pole_matches_forward_in_opposite_heading():
    report = rover(1, SOUTH_ROW, "N").execute("B")
    assert report.position == (5, SOUTH_ROW)
    assert report.heading == "N"


def test_forward_then_backward_crosses_back_and_faces_away_from_the_pole():
    report = rover(2, NORTH_ROW, "N").execute("FB")
    assert report.position == (2, NORTH_ROW)
    assert report.heading == "S"


def test_after_crossing_forward_heads_toward_the_equator():
    report = rover(2, NORTH_ROW, "N").execute("FF")
    assert report.position == (6, NORTH_ROW - 1)
    assert report.heading == "S"


def test_moving_along_a_pole_row_still_wraps_longitude():
    assert rover(WIDTH - 1, NORTH_ROW, "E").execute("F").position == (0, NORTH_ROW)


def test_leaving_the_pole_row_toward_the_equator_is_a_plain_move():
    report = rover(2, NORTH_ROW, "S").execute("F")
    assert report.position == (2, NORTH_ROW - 1)
    assert report.heading == "S"


def test_crossing_continues_the_command_string():
    report = rover(0, NORTH_ROW, "N").execute("FFF")
    assert report.position == (4, NORTH_ROW - 2)
    assert report.heading == "S"


def test_obstacle_on_the_far_side_of_the_pole_blocks_the_crossing():
    r = rover(0, NORTH_ROW, "N", obstacles=[(4, NORTH_ROW)])
    report = r.execute("F")
    assert report.blocked_by == (4, NORTH_ROW)
    assert report.position == (0, NORTH_ROW)
    assert report.heading == "N"
    assert r.discovered_obstacles() == [(4, NORTH_ROW)]


def test_single_row_planet_treats_every_latitude_move_as_a_crossing():
    r = Rover(Planet(4, 1), 0, 0, "N")
    report = r.execute("F")  # north pole crossing
    assert (report.position, report.heading) == ((2, 0), "S")
    report = r.execute("F")  # now a south pole crossing
    assert (report.position, report.heading) == ((0, 0), "N")
    report = r.execute("B")  # backward across the south pole
    assert (report.position, report.heading) == ((2, 0), "N")


def test_two_column_planet_swaps_columns_at_the_pole():
    report = Rover(Planet(2, 3), 1, 2, "N").execute("F")
    assert (report.position, report.heading) == ((0, 2), "S")
