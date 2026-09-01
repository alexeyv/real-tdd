from mars_rover import Rover


def test_new_rover_reports_its_starting_position_and_heading():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    assert rover.position == (2, 3)
    assert rover.heading == "N"


def test_turning_left_from_north_heads_west():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("L")

    assert rover.heading == "W"


def test_turning_left_from_west_heads_south():
    rover = Rover(width=10, height=10, x=2, y=3, heading="W")

    rover.execute("L")

    assert rover.heading == "S"


def test_turning_right_from_north_heads_east():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("R")

    assert rover.heading == "E"


def test_moving_forward_heading_north_increases_latitude():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("F")

    assert rover.position == (2, 4)


def test_moving_forward_heading_east_increases_longitude():
    rover = Rover(width=10, height=10, x=2, y=3, heading="E")

    rover.execute("F")

    assert rover.position == (3, 3)


def test_a_command_string_runs_its_commands_in_order():
    rover = Rover(width=10, height=10, x=0, y=0, heading="N")

    rover.execute("FFRFF")

    assert rover.position == (2, 2)
    assert rover.heading == "E"


def test_moving_backward_goes_opposite_the_heading_without_turning():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("B")

    assert rover.position == (2, 2)
    assert rover.heading == "N"


def test_moving_east_off_the_last_column_wraps_to_the_first():
    rover = Rover(width=10, height=10, x=9, y=3, heading="E")

    rover.execute("F")

    assert rover.position == (0, 3)


def test_moving_north_off_the_north_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=5, x=2, y=4, heading="N")

    rover.execute("F")

    assert rover.position == (7, 4)
    assert rover.heading == "S"


def test_moving_forward_heading_south_decreases_latitude():
    rover = Rover(width=10, height=10, x=2, y=3, heading="S")

    rover.execute("F")

    assert rover.position == (2, 2)


def test_moving_south_off_the_south_pole_row_crosses_the_pole():
    rover = Rover(width=10, height=5, x=2, y=0, heading="S")

    rover.execute("F")

    assert rover.position == (7, 0)
    assert rover.heading == "N"


def test_moving_forward_heading_west_decreases_longitude():
    rover = Rover(width=10, height=10, x=2, y=3, heading="W")

    rover.execute("F")

    assert rover.position == (1, 3)


def test_moving_into_an_unknown_obstacle_leaves_the_rover_in_place():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.position == (2, 3)


def test_the_rover_reports_the_obstacle_it_stopped_at():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.stopped_by == (2, 4)


def test_a_bump_abandons_the_rest_of_the_command_string():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("FR")

    assert rover.heading == "N"


def test_a_rover_that_has_hit_nothing_reports_no_obstacle():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("FF")

    assert rover.stopped_by is None


def test_a_new_rover_has_discovered_no_obstacles():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    assert rover.discovered_obstacles == ()


def test_bumping_an_obstacle_discovers_it():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")

    assert rover.discovered_obstacles == ((2, 4),)


def test_bumping_the_same_obstacle_twice_lists_it_once():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("F")
    rover.execute("F")

    assert rover.discovered_obstacles == ((2, 4),)


def test_a_command_string_that_would_hit_a_known_obstacle_is_refused_whole():
    rover = Rover(width=10, height=10, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.position == (2, 3)


def test_a_later_command_string_does_not_still_report_an_earlier_bump():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})
    rover.execute("F")

    rover.execute("R")

    assert rover.stopped_by is None


def test_a_refused_command_string_reports_the_known_obstacle_in_the_way():
    rover = Rover(width=10, height=10, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.stopped_by == (2, 5)


def test_an_unknown_obstacle_before_a_known_one_is_bumped_not_refused():
    rover = Rover(width=10, height=10, x=1, y=6, heading="E", obstacles={(2, 5), (2, 6)})
    rover.execute("F")
    rover.execute("RFFFLFL")

    rover.execute("FFF")

    assert rover.position == (2, 4)
    assert rover.stopped_by == (2, 5)


# Regression tests. Each of these passed the moment it was written: the
# behaviour it pins down was already there, put in place by a
# generalisation made for some earlier test. None of them is a step.


def test_turning_left_all_the_way_round_the_compass():
    rover = Rover(width=10, height=10, x=2, y=3, heading="S")

    rover.execute("L")
    assert rover.heading == "E"
    rover.execute("L")
    assert rover.heading == "N"


def test_turning_right_all_the_way_round_the_compass():
    rover = Rover(width=10, height=10, x=2, y=3, heading="E")

    rover.execute("R")
    assert rover.heading == "S"
    rover.execute("R")
    assert rover.heading == "W"
    rover.execute("R")
    assert rover.heading == "N"


def test_turning_leaves_the_position_alone():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("LRRL")

    assert rover.position == (2, 3)


def test_moving_west_off_column_zero_wraps_to_the_last_column():
    rover = Rover(width=10, height=10, x=0, y=3, heading="W")

    rover.execute("F")

    assert rover.position == (9, 3)


def test_moving_backward_wraps_longitude_too():
    rover = Rover(width=10, height=10, x=0, y=3, heading="E")

    rover.execute("B")

    assert rover.position == (9, 3)


def test_backing_over_the_north_pole_crosses_it():
    rover = Rover(width=10, height=5, x=2, y=4, heading="S")

    rover.execute("B")

    assert rover.position == (7, 4)
    assert rover.heading == "N"


def test_backing_over_the_south_pole_crosses_it():
    rover = Rover(width=10, height=5, x=2, y=0, heading="N")

    rover.execute("B")

    assert rover.position == (7, 0)
    assert rover.heading == "S"


def test_crossing_the_same_pole_twice_returns_to_the_original_longitude():
    rover = Rover(width=10, height=5, x=2, y=4, heading="N")

    rover.execute("F")
    rover.execute("LL")
    rover.execute("F")

    assert rover.position == (2, 4)


def test_crossing_the_pole_near_the_wrap_edge_lands_on_the_far_side():
    rover = Rover(width=10, height=5, x=8, y=4, heading="N")

    rover.execute("F")

    assert rover.position == (3, 4)
    assert rover.heading == "S"


def test_moving_backward_into_an_unknown_obstacle_stops_the_rover():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 2)})

    rover.execute("B")

    assert rover.position == (2, 3)
    assert rover.stopped_by == (2, 2)


def test_the_commands_before_a_bump_are_carried_out():
    rover = Rover(width=10, height=10, x=2, y=1, heading="N", obstacles={(2, 4)})

    rover.execute("FFFF")

    assert rover.position == (2, 3)


def test_an_obstacle_on_the_far_side_of_a_pole_stops_the_crossing():
    rover = Rover(width=10, height=5, x=2, y=4, heading="N", obstacles={(7, 4)})

    rover.execute("F")

    assert rover.position == (2, 4)
    assert rover.heading == "N"
    assert rover.stopped_by == (7, 4)


def test_an_obstacle_across_the_wrap_stops_the_rover():
    rover = Rover(width=10, height=10, x=9, y=3, heading="E", obstacles={(0, 3)})

    rover.execute("F")

    assert rover.position == (9, 3)
    assert rover.stopped_by == (0, 3)


def test_turning_beside_an_obstacle_never_bumps():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})

    rover.execute("RLLR")

    assert rover.heading == "N"
    assert rover.stopped_by is None
    assert rover.discovered_obstacles == ()


def test_discovered_obstacles_are_listed_in_the_order_they_were_found():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4), (3, 3)})

    rover.execute("F")
    rover.execute("RF")

    assert rover.discovered_obstacles == ((2, 4), (3, 3))


def test_a_refused_command_string_leaves_the_heading_alone():
    rover = Rover(width=10, height=10, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("RLFF")

    assert rover.heading == "N"
    assert rover.position == (2, 3)


def test_refusal_looks_ahead_past_turns_and_a_pole_crossing():
    rover = Rover(width=10, height=5, x=2, y=4, heading="N", obstacles={(7, 3)})
    rover.execute("FF")
    rover.execute("LL")

    rover.execute("RRF")

    assert rover.position == (7, 4)
    assert rover.heading == "N"
    assert rover.stopped_by == (7, 3)


def test_a_string_of_only_turns_is_never_refused():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N", obstacles={(2, 4)})
    rover.execute("F")

    rover.execute("RL")

    assert rover.heading == "N"
    assert rover.stopped_by is None


def test_a_refused_command_string_discovers_nothing_new():
    rover = Rover(width=10, height=10, x=2, y=4, heading="N", obstacles={(2, 5)})
    rover.execute("F")
    rover.execute("B")

    rover.execute("FF")

    assert rover.discovered_obstacles == ((2, 5),)


def test_an_empty_command_string_changes_nothing():
    rover = Rover(width=10, height=10, x=2, y=3, heading="N")

    rover.execute("")

    assert rover.position == (2, 3)
    assert rover.heading == "N"
    assert rover.stopped_by is None
