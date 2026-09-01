from mars_rover import Rover


def test_new_rover_reports_its_position_and_heading():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    assert rover.position == (2, 3)
    assert rover.heading == "N"


def test_forward_facing_north_moves_one_row_north():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("F")

    assert rover.position == (2, 4)
    assert rover.heading == "N"


def test_forward_facing_east_moves_one_column_east():
    rover = Rover(width=10, height=6, x=2, y=3, heading="E")

    rover.execute("F")

    assert rover.position == (3, 3)
    assert rover.heading == "E"


def test_forward_facing_south_moves_one_row_south():
    rover = Rover(width=10, height=6, x=2, y=3, heading="S")

    rover.execute("F")

    assert rover.position == (2, 2)
    assert rover.heading == "S"


def test_left_turn_facing_north_ends_facing_west_without_moving():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("L")

    assert rover.heading == "W"
    assert rover.position == (2, 3)


def test_commands_in_a_string_are_executed_in_order():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("FL")

    assert rover.position == (2, 4)
    assert rover.heading == "W"


def test_forward_east_off_the_last_column_lands_on_column_zero():
    rover = Rover(width=10, height=6, x=9, y=3, heading="E")

    rover.execute("F")

    assert rover.position == (0, 3)


def test_forward_facing_west_moves_one_column_west():
    rover = Rover(width=10, height=6, x=2, y=3, heading="W")

    rover.execute("F")

    assert rover.position == (1, 3)
    assert rover.heading == "W"


def test_forward_west_off_column_zero_lands_on_the_last_column():
    rover = Rover(width=10, height=6, x=0, y=3, heading="W")

    rover.execute("F")

    assert rover.position == (9, 3)


def test_backward_facing_north_moves_one_row_south():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("B")

    assert rover.position == (2, 2)
    assert rover.heading == "N"


def test_right_turn_facing_north_ends_facing_east_without_moving():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("R")

    assert rover.heading == "E"
    assert rover.position == (2, 3)


def test_forward_into_an_obstacle_does_not_move_the_rover():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.position == (2, 3)


def test_hitting_an_obstacle_abandons_the_rest_of_the_commands():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("FL")

    assert rover.position == (2, 3)
    assert rover.heading == "N"


def test_rover_reports_the_obstacle_that_stopped_it():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.blocked_by == (2, 4)


def test_rover_reports_no_obstacle_after_commands_that_hit_nothing():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")

    rover.execute("F")

    assert rover.blocked_by is None


def test_commands_that_hit_nothing_clear_an_earlier_obstacle_report():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})
    rover.execute("F")

    rover.execute("R")

    assert rover.blocked_by is None


def test_forward_north_from_the_north_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=6, x=2, y=5, heading="N")

    rover.execute("F")

    assert rover.position == (7, 5)
    assert rover.heading == "S"


def test_backward_over_the_north_pole_flips_longitude_and_heading():
    rover = Rover(width=10, height=6, x=2, y=5, heading="S")

    rover.execute("B")

    assert rover.position == (7, 5)
    assert rover.heading == "N"


def test_forward_south_from_the_south_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=6, x=2, y=0, heading="S")

    rover.execute("F")

    assert rover.position == (7, 0)
    assert rover.heading == "N"


def test_backward_over_the_south_pole_flips_longitude_and_heading():
    rover = Rover(width=10, height=6, x=2, y=0, heading="N")

    rover.execute("B")

    assert rover.position == (7, 0)
    assert rover.heading == "S"


def test_new_rover_has_discovered_no_obstacles():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    assert rover.discovered_obstacles == []


def test_an_obstacle_the_rover_bumps_into_is_remembered():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.discovered_obstacles == [(2, 4)]


def test_bumping_the_same_obstacle_again_does_not_record_it_twice():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})
    rover.execute("F")

    rover.execute("F")

    assert rover.discovered_obstacles == [(2, 4)]


def test_commands_that_would_hit_a_known_obstacle_are_refused_without_moving():
    rover = Rover(width=10, height=6, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.position == (2, 3)


def test_refused_commands_report_the_known_obstacle_they_would_have_hit():
    rover = Rover(width=10, height=6, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.refused_by == (2, 5)


def test_left_turn_facing_west_ends_facing_south():
    rover = Rover(width=10, height=6, x=2, y=3, heading="W")

    rover.execute("L")

    assert rover.heading == "S"


def test_four_left_turns_pass_through_every_heading_and_return_to_north():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")
    seen = []

    for _ in range(4):
        rover.execute("L")
        seen.append(rover.heading)

    assert seen == ["W", "S", "E", "N"]


def test_four_right_turns_pass_through_every_heading_and_return_to_north():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N")
    seen = []

    for _ in range(4):
        rover.execute("R")
        seen.append(rover.heading)

    assert seen == ["E", "S", "W", "N"]


def test_turning_next_to_an_obstacle_hits_nothing():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("LR")

    assert rover.blocked_by is None
    assert rover.heading == "N"
    assert rover.discovered_obstacles == []


def test_an_obstacle_on_the_far_side_of_the_pole_stops_the_crossing():
    rover = Rover(width=10, height=6, x=2, y=5, heading="N", obstacles={(7, 5)})

    rover.execute("F")

    assert rover.position == (2, 5)
    assert rover.heading == "N"
    assert rover.blocked_by == (7, 5)


def test_discovered_obstacles_are_reported_in_discovery_order():
    rover = Rover(width=10, height=6, x=2, y=3, heading="N", obstacles={(2, 4), (3, 3)})
    rover.execute("F")

    rover.execute("RF")

    assert rover.discovered_obstacles == [(2, 4), (3, 3)]


def test_refused_commands_do_not_change_the_heading_either():
    rover = Rover(width=10, height=6, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("LLBB")

    assert rover.heading == "N"
    assert rover.position == (2, 3)


def test_refused_by_is_none_after_commands_that_were_not_refused():
    rover = Rover(width=10, height=6, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")
    rover.execute("FF")

    rover.execute("R")

    assert rover.refused_by is None


def test_turning_next_to_a_known_obstacle_is_not_refused():
    rover = Rover(width=10, height=6, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")

    rover.execute("LLLL")

    assert rover.refused_by is None
    assert rover.heading == "N"


def test_commands_toward_an_unknown_obstacle_are_not_refused_but_stop_at_the_bump():
    rover = Rover(width=10, height=6, x=2, y=1, heading="N", obstacles={(2, 4)})

    rover.execute("FFFF")

    assert rover.refused_by is None
    assert rover.position == (2, 3)
    assert rover.blocked_by == (2, 4)
