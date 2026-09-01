from mars_rover import Rover


def test_new_rover_reports_the_position_and_heading_it_was_created_with():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_forward_moves_one_square_north_when_heading_north():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 3, "N")


def test_forward_moves_one_square_east_when_heading_east():
    rover = Rover(width=10, height=6, x=3, y=2, heading="E")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (4, 2, "E")


def test_left_turns_the_rover_from_north_to_west():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("L")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "W")


def test_right_turns_the_rover_from_north_to_east():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("R")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "E")


def test_moving_east_off_the_last_column_wraps_to_column_zero():
    rover = Rover(width=10, height=6, x=9, y=2, heading="E")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (0, 2, "E")


def test_backward_moves_one_square_south_when_heading_north():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("B")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "N")


def test_forward_moves_one_square_south_when_heading_south():
    rover = Rover(width=10, height=6, x=3, y=2, heading="S")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "S")


def test_forward_moves_one_square_west_when_heading_west():
    rover = Rover(width=10, height=6, x=3, y=2, heading="W")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (2, 2, "W")


def test_a_command_string_is_executed_one_command_after_another():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N")

    rover.execute("FFRFF")

    assert (rover.x, rover.y, rover.heading) == (5, 4, "E")


def test_forward_off_the_north_pole_row_crosses_the_pole_heading_south():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (8, 5, "S")


def test_forward_off_the_south_pole_row_crosses_the_pole_heading_north():
    rover = Rover(width=10, height=6, x=3, y=0, heading="S")

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (8, 0, "N")


def test_backward_off_the_north_pole_row_crosses_the_pole_like_a_forward_move():
    rover = Rover(width=10, height=6, x=3, y=5, heading="S")

    rover.execute("B")

    assert (rover.x, rover.y, rover.heading) == (8, 5, "N")


def test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_a_move_onto_an_obstacle_abandons_the_rest_of_the_command_string():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    rover.execute("FR")

    assert (rover.x, rover.y, rover.heading) == (3, 2, "N")


def test_after_hitting_an_obstacle_the_rover_reports_which_obstacle_it_was():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    rover.execute("F")

    assert rover.blocked_by == (3, 3)


def test_after_a_command_string_that_hits_nothing_the_rover_reports_no_obstacle():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})
    rover.execute("F")

    rover.execute("RF")

    assert (rover.x, rover.y, rover.blocked_by) == (4, 2, None)


def test_turning_never_hits_an_obstacle():
    rover = Rover(
        width=10,
        height=6,
        x=3,
        y=2,
        heading="N",
        obstacles={(3, 3), (3, 1), (2, 2), (4, 2)},
    )

    rover.execute("LLRR")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 2, "N", None)


def test_an_obstacle_across_the_pole_stops_the_crossing_and_the_rover_stays_put():
    rover = Rover(width=10, height=6, x=3, y=5, heading="N", obstacles={(8, 5)})

    rover.execute("F")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 5, "N", (8, 5))


def test_a_new_rover_has_discovered_no_obstacles():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    assert rover.discovered_obstacles == ()


def test_bumping_into_an_unknown_obstacle_discovers_it():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    rover.execute("F")

    assert rover.discovered_obstacles == ((3, 3),)


def test_bumping_into_the_same_obstacle_twice_records_it_once():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})
    rover.execute("F")

    rover.execute("F")

    assert rover.discovered_obstacles == ((3, 3),)


def test_discovered_obstacles_come_back_in_the_order_they_were_discovered():
    rover = Rover(width=10, height=6, x=3, y=2, heading="E", obstacles={(4, 2), (3, 3)})
    rover.execute("F")

    rover.execute("LF")

    assert rover.discovered_obstacles == ((4, 2), (3, 3))


def test_a_command_string_that_would_hit_a_known_obstacle_is_refused_before_it_moves():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert (rover.x, rover.y, rover.heading) == (3, 1, "N")


def test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.blocked_by == (3, 3)


def test_a_command_string_of_turns_alone_is_never_refused():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})
    rover.execute("F")

    rover.execute("LLRR")

    assert (rover.x, rover.y, rover.heading, rover.blocked_by) == (3, 2, "N", None)


def test_a_rover_that_has_not_run_a_command_string_reports_no_obstacle():
    rover = Rover(width=10, height=6, x=3, y=2, heading="N", obstacles={(3, 3)})

    assert rover.blocked_by is None
