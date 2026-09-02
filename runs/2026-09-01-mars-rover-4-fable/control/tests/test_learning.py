"""Twist 2: the rover starts with no map and learns obstacles by bumping."""

from mars_rover import Planet, Rover


def rover(x=0, y=0, heading="N", obstacles=()):
    return Rover(Planet(10, 10, obstacles), x, y, heading)


def test_starts_with_no_known_obstacles():
    assert rover(obstacles=[(0, 1)]).discovered_obstacles() == []


def test_first_bump_into_an_unknown_obstacle_is_the_classic_stop():
    r = rover(0, 0, "N", obstacles=[(0, 2)])
    report = r.execute("FFF")
    assert report.position == (0, 1)
    assert report.blocked_by == (0, 2)
    assert not report.refused


def test_remembers_obstacles_in_discovery_order():
    r = rover(0, 0, "N", obstacles=[(0, 1), (1, 0)])
    r.execute("F")
    r.execute("RF")
    assert r.discovered_obstacles() == [(0, 1), (1, 0)]


def test_trying_a_known_obstacle_again_does_not_record_it_twice():
    r = rover(0, 0, "N", obstacles=[(0, 1)])
    assert not r.execute("F").refused
    assert r.execute("F").refused
    assert r.discovered_obstacles() == [(0, 1)]


def test_bumping_the_same_obstacle_via_a_different_approach_records_it_once():
    r = rover(0, 0, "N", obstacles=[(1, 1)])
    r.execute("RFLF")  # east to (1,0), face N, bump (1,1)
    r.execute("RFLFL")  # east to (2,0), face N, forward to (2,1), face W: next F would bump (1,1)
    assert r.discovered_obstacles() == [(1, 1)]
    report = r.execute("F")
    assert report.refused
    assert report.blocked_by == (1, 1)
    assert r.discovered_obstacles() == [(1, 1)]


def test_known_obstacle_refuses_whole_string_without_moving():
    r = rover(0, 0, "N", obstacles=[(0, 3)])
    r.execute("FFFF")  # ends at (0, 2), learns (0, 3)
    r.execute("BB")  # back to (0, 0)
    report = r.execute("FFFFRF")
    assert report.refused
    assert report.blocked_by == (0, 3)
    assert report.stopped_by_obstacle
    assert report.position == (0, 0)
    assert report.heading == "N"
    assert r.position == (0, 0)
    assert r.heading == "N"


def test_refusal_reports_the_first_known_obstacle_on_the_path():
    r = rover(0, 0, "N", obstacles=[(0, 1), (1, 0)])
    r.execute("F")
    r.execute("RF")
    report = r.execute("FL")
    assert report.blocked_by == (1, 0)


def test_known_obstacle_off_the_path_does_not_refuse():
    r = rover(0, 0, "N", obstacles=[(0, 1)])
    r.execute("F")
    report = r.execute("RFLF")
    assert not report.refused
    assert report.position == (1, 1)


def test_turning_is_fine_even_when_facing_a_known_obstacle():
    r = rover(0, 0, "N", obstacles=[(0, 1)])
    r.execute("F")
    report = r.execute("LRRL")
    assert not report.refused
    assert not report.stopped_by_obstacle
    assert report.heading == "N"


def test_prediction_accounts_for_pole_crossing():
    r = Rover(Planet(8, 3, obstacles=[(4, 2)]), 0, 2, "N")
    r.execute("F")  # bump the far side of the north pole, learn it
    assert r.discovered_obstacles() == [(4, 2)]
    report = r.execute("LLRRF")
    assert report.refused
    assert report.blocked_by == (4, 2)


def test_prediction_uses_only_the_rovers_own_map():
    # An unknown obstacle at (0, 1) sits before the known one at (0, 3); the
    # rover cannot see it, so it still refuses on the known obstacle.
    planet = Planet(10, 10, obstacles=[(0, 1), (0, 3)])
    scout = Rover(planet, 0, 2, "N")
    scout.execute("F")  # learn (0, 3)
    assert scout.discovered_obstacles() == [(0, 3)]
    scout.execute("RRF")  # face S; (0,1) is unknown so this bumps and learns it
    assert scout.discovered_obstacles() == [(0, 3), (0, 1)]

    r = Rover(planet, 0, 2, "N")
    r.execute("F")  # learn (0, 3) only
    r.execute("RFLBBLFR")  # detour around (0, 1) back to (0, 0), facing N
    assert (r.position, r.heading) == ((0, 0), "N")
    assert r.discovered_obstacles() == [(0, 3)]
    report = r.execute("FFF")
    assert report.refused
    assert report.blocked_by == (0, 3)
    assert r.position == (0, 0)


def test_discovered_obstacles_is_a_copy():
    r = rover(0, 0, "N", obstacles=[(0, 1)])
    r.execute("F")
    r.discovered_obstacles().clear()
    assert r.discovered_obstacles() == [(0, 1)]


def test_prediction_follows_longitude_wrap_and_a_backward_crossing():
    # Known obstacle at (5, 2) on the north pole row of an 8-wide planet.
    planet = Planet(8, 3, obstacles=[(5, 2)])
    r = Rover(planet, 5, 1, "N")
    r.execute("F")  # bump (5, 2) from below, learn it
    assert r.discovered_obstacles() == [(5, 2)]
    r.execute("RFFL")  # (7, 1) facing N
    r.execute("F")  # (7, 2) on the pole row
    assert (r.position, r.heading) == ((7, 2), "N")
    # Path: R -> E, F wraps to (0, 2), F to (1, 2), R -> S, B crosses the
    # pole backward to (5, 2), which is known: refuse without moving.
    report = r.execute("RFFRB")
    assert report.refused
    assert report.blocked_by == (5, 2)
    assert (r.position, r.heading) == ((7, 2), "N")
    # The same path with one fewer eastward step lands at (4, 2) instead.
    report = r.execute("RFRB")
    assert not report.refused
    assert (report.position, report.heading) == ((4, 2), "S")
