from mars_rover import Rover


def test_rover_reports_the_position_and_heading_it_was_created_with():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_moving_forward_facing_north_raises_latitude_by_one():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 3, "N")


def test_moving_forward_facing_south_lowers_latitude_by_one():
    rover = Rover(width=10, height=6, x=3, y=2, heading="S")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "S")


def test_turning_left_from_north_faces_west_without_moving():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("L")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "W")


def test_turning_left_from_west_faces_south():
    rover = Rover(width=10, height=6, x=3, y=2, heading="W")

    rover.execute("L")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "S")


def test_moving_forward_facing_east_raises_longitude_by_one():
    rover = Rover(width=10, height=6, x=3, y=2, heading="E")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (4, 2, "E")


def test_turning_right_from_north_faces_east_without_moving():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("R")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "E")


def test_commands_are_executed_in_the_order_given():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("RF")

    assert (rover.x, rover.y, rover.heading) == (4, 2, "E")


def test_turning_left_four_times_returns_to_the_original_heading():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("LLLL")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_moving_east_off_the_last_column_lands_on_column_zero():
    rover = Rover(width=10, height=6, x=9, y=2, heading="E")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (0, 2, "E")


def test_turning_right_from_east_faces_south():
    rover = Rover(width=10, height=6, x=3, y=2, heading="E")

    rover.execute("R")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "S")


def test_moving_backward_facing_north_lowers_latitude_by_one():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("B")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "N")


def test_moving_forward_facing_west_lowers_longitude_by_one():
    rover = Rover(width=10, height=6, x=3, y=2, heading="W")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (2, 2, "W")


def test_moving_west_off_column_zero_lands_on_the_last_column():
    rover = Rover(width=10, height=6, x=0, y=2, heading="W")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (9, 2, "W")


def test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_a_move_blocked_by_an_obstacle_abandons_the_rest_of_the_commands():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])

    rover.execute("FR")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_after_a_blocked_command_string_the_rover_reports_which_obstacle():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])

    rover.execute("F")

    assert rover.blocked_by == (3, 3)


def test_after_an_unblocked_command_string_no_obstacle_is_reported():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(7, 7)])

    rover.execute("F")

    assert rover.blocked_by is None


def test_a_later_unblocked_command_string_clears_the_obstacle_report():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])
    rover.execute("F")

    rover.execute("RF")

    assert rover.blocked_by is None


def test_an_empty_command_string_leaves_the_rover_where_it_was():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_turning_to_face_an_obstacle_is_not_blocked():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(4, 2)])

    rover.execute("R")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 2, "E", None)


def test_moving_north_off_the_north_pole_row_stays_on_that_row():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N")

    rover.execute("F")

    assert rover.y == 5


def test_crossing_the_north_pole_puts_the_rover_on_the_far_side():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N")

    rover.execute("F")

    assert rover.x == 8


def test_crossing_the_north_pole_turns_the_rover_south():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N")

    rover.execute("F")

    assert rover.heading == "S"


def test_moving_south_off_the_south_pole_row_crosses_the_south_pole():
    rover = Rover(width=10, height=6, x=3, y=0, heading="S")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (8, 0, "N")


def test_backing_off_the_north_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=6, x=3, y=5, heading="S")

    rover.execute("B")

    assert (rover.x, rover.y, rover.heading) == (8, 5, "N")


def test_backing_off_the_south_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N")

    rover.execute("B")

    assert (rover.x, rover.y, rover.heading) == (8, 0, "S")


def test_an_obstacle_on_the_far_side_of_the_pole_blocks_the_crossing():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N", obstacles=[(8, 5)])

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 5, "N", (8, 5))


def test_a_new_rover_has_discovered_no_obstacles():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])

    assert rover.discovered == []


def test_an_obstacle_the_rover_bumps_into_is_remembered():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])

    rover.execute("F")

    assert rover.discovered == [(3, 3)]


def test_bumping_into_the_same_obstacle_twice_records_it_once():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3)])
    rover.execute("F")

    rover.execute("F")

    assert rover.discovered == [(3, 3)]


def test_discovered_obstacles_are_reported_in_the_order_they_were_found():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles=[(3, 3), (4, 2)])
    rover.execute("F")

    rover.execute("RF")

    assert rover.discovered == [(3, 3), (4, 2)]


def test_a_command_string_that_would_hit_a_known_obstacle_is_refused_as_a_whole():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3)])
    rover.execute("FFF")
    rover.execute("B")

    rover.execute("FF")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "N")


def test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3)])
    rover.execute("FFF")
    rover.execute("B")

    rover.execute("FF")

    assert rover.blocked_by == (3, 3)


def test_a_command_string_is_refused_for_a_known_obstacle_it_would_hit_later_on():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3)])
    rover.execute("FFF")
    rover.execute("BB")

    rover.execute("FFFF")

    assert (rover.x, rover.y, rover.heading) == (3, 0, "N")


def test_a_command_string_that_turns_away_from_a_known_obstacle_is_not_refused():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3)])
    rover.execute("FFF")

    rover.execute("RF")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (4, 2, "E", None)


def test_a_command_string_of_only_turns_is_never_refused():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3)])
    rover.execute("FFF")

    rover.execute("RRRR")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 2, "N", None)


def test_a_refused_command_string_discovers_nothing_new():
    rover = Rover(width=10, height=6, x=3, y=0, heading="N", obstacles=[(3, 3), (3, 4)])
    rover.execute("FFF")
    rover.execute("B")

    rover.execute("FF")

    assert rover.discovered == [(3, 3)]


def test_a_known_obstacle_reached_only_by_wrapping_is_seen_in_advance():
    rover = Rover(width=10, height=6, x=8, y=2, heading="E", obstacles=[(1, 2)])
    rover.execute("FFF")
    rover.execute("BB")

    rover.execute("FFF")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (8, 2, "E", (1, 2))
