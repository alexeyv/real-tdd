# Journal

Run 4. Task: Mars Rover with real poles and a learning rover. Python 3,
pytest, in a `.venv` at the repo root (`.venv/bin/python -m pytest -q`).

## Turn 1 — ping

**Received:** nothing; run start. Scaffolding commit 34f86a2 (pyproject
pytest config, empty `tests/` package). No production code.
**Green by:** n/a
**Refactored:** nothing
**Commit:** 34f86a2 (scaffolding only)
**Also satisfied:** none
**Wrote:** `test_new_rover_reports_its_position_and_heading` — fails
because `ModuleNotFoundError: No module named 'mars_rover'` at collection.
**Interface decided:** package `mars_rover` exporting class `Rover`;
constructor keywords `width`, `height`, `x`, `y`, `heading`; heading is a
one-letter string `"N"`/`"E"`/`"S"`/`"W"`; `rover.position` is an
`(x, y)` tuple; `rover.heading` is the letter.
**List:** checked "A rover created with a position and heading reports
that position and heading". Added no items.
**Surprise:** none. One reading I fixed in the list rather than asking:
"backward moves cross the pole the same way a forward move in the
opposite heading would" I read as "the outcome is identical to that
forward move", so a rover heading S that backs over the north pole ends
up heading S on the far side. That is also what a physical rover would
do. If that reading is wrong, the list item is the place to correct it.

## Turn 2 — pong

**Received:** `test_new_rover_reports_its_position_and_heading` failing because `ModuleNotFoundError: No module named 'mars_rover'` at collection.
**Green by:** Obvious Implementation — a class that stores the two constructor values is the whole behavior; nothing to fake.
**Refactored:** nothing
**Commit:** 97b28ad
**Also satisfied:** none
**Wrote:** `test_forward_facing_north_moves_one_row_north` — fails because `AttributeError: 'Rover' object has no attribute 'execute'`.
**Interface decided:** `rover.execute(commands: str)` runs a command string; return value not asserted. Position and heading are read back through the existing attributes.
**List:** checked "`F` moves one square forward in the current heading (north increases `y`, ...)" for the north case; added "`F` moves one square forward when heading E, S, or W" so the other headings stay on the list.
**Surprise:** none.

## Turn 3 — ping

**Received:** `test_forward_facing_north_moves_one_row_north` failing because `AttributeError: 'Rover' object has no attribute 'execute'`. Also received the human's clarification appended to `task.md`: a backward pole crossing flips the heading like a forward one does. Updated the test list item to say so and committed the task change with this green.
**Green by:** Obvious Implementation — `execute` adds one to `y`; the only test demands nothing else, so no heading dispatch yet.
**Refactored:** nothing
**Commit:** 9668f94
**Also satisfied:** none
**Wrote:** `test_forward_facing_east_moves_one_column_east` — fails because `assert (2, 4) == (3, 3)`: the rover went north regardless of heading.
**Interface decided:** none new.
**List:** checked the E case of forward movement; split S and W into their own remaining item.
**Surprise:** none. The east test at the same start square as the north test is a deliberate second point on the heading axis, so the next green has to consult the heading.

## Turn 4 — pong

**Received:** `test_forward_facing_east_moves_one_column_east` failing because `assert (2, 4) == (3, 3)`: `execute` always added one to `y`.
**Green by:** Triangulate — two tests at the same square with different headings forced a heading lookup; the step table holds only N and E because no test asks for more.
**Refactored:** nothing
**Commit:** 29baab2
**Also satisfied:** none
**Wrote:** `test_forward_facing_south_moves_one_row_south` — fails because `KeyError: 'S'` in the step table.
**Interface decided:** none new.
**List:** checked the S case of forward movement; W remains as its own item.
**Surprise:** none. Read the human's clarification on backward pole crossings; the list item ping rewrote already carries it.

## Turn 5 — ping

**Received:** `test_forward_facing_south_moves_one_row_south` failing because `KeyError: 'S'` in the step table.
**Green by:** Obvious Implementation — one more row in the step table.
**Refactored:** nothing
**Commit:** bf38267
**Also satisfied:** none
**Wrote:** `test_left_turn_facing_north_ends_facing_west_without_moving` — fails because `assert 'N' == 'W'`: `execute` ignores the command letter and always steps forward, so the rover moved north and kept its heading. (The heading assert fires first; the position would also be wrong.)
**Interface decided:** none new.
**List:** checked the N -> W case of `L`; split the other three left turns into their own item. Left W on the forward list untouched; it is one table row and can be picked whenever.
**Surprise:** none. Chose a turn rather than the W forward step because a turn is the first test that makes `execute` read the command letter at all.

## Turn 6 — pong

**Received:** `test_left_turn_facing_north_ends_facing_west_without_moving` failing because `assert 'N' == 'W'`: `execute` never looked at the command letter.
**Green by:** Obvious Implementation — branch on the command letter; a left-turn table with only the N row, since that is all the test demands.
**Refactored:** nothing
**Commit:** 422e749
**Also satisfied:** none
**Wrote:** `test_commands_in_a_string_are_executed_in_order` — fails because `assert 'N' == 'W'`: `"FL"` is not `"L"`, so the whole string was treated as a forward step and the turn never happened.
**Interface decided:** none new.
**List:** checked "The commands in a string are executed in order".
**Surprise:** none. Picked ordering over the remaining single-letter table rows because it is the first test that makes `execute` loop.

## Turn 7 — ping

**Received:** `test_commands_in_a_string_are_executed_in_order` failing because `assert 'N' == 'W'`: `execute` compared the whole string to `"L"`.
**Green by:** Obvious Implementation — loop over the string, branch per letter.
**Refactored:** nothing
**Commit:** 8e50f35
**Also satisfied:** none
**Wrote:** `test_forward_east_off_the_last_column_lands_on_column_zero` — fails because `assert (10, 3) == (0, 3)`: the rover walked off the map; `width` has never been read.
**Interface decided:** none new.
**List:** checked "Moving east off the last column lands on column 0".
**Surprise:** none. This is the first test that gives `width` a job.

## Turn 8 — pong

**Received:** `test_forward_east_off_the_last_column_lands_on_column_zero` failing because `assert (10, 3) == (0, 3)`: `width` was never stored or read.
**Green by:** Obvious Implementation — keep `width` and reduce the new `x` modulo it.
**Refactored:** nothing
**Commit:** 5c3e121
**Also satisfied:** none by test, but the modulo is Python's, so "Moving west off column 0 lands on the last column" will likely pass as soon as the W step exists. Left it on the list for whoever writes it to find out.
**Wrote:** `test_forward_facing_west_moves_one_column_west` — fails because `KeyError: 'W'` in the step table.
**Interface decided:** none new.
**List:** checked "`F` moves one square forward when heading W".
**Surprise:** none. Picked the W step before the west wrap so the wrap test cannot fail for the wrong reason.

## Turn 9 — ping

**Received:** `test_forward_facing_west_moves_one_column_west` failing because `KeyError: 'W'` in the step table.
**Green by:** Obvious Implementation — one more table row.
**Refactored:** nothing
**Commit:** 35edf5a
**Also satisfied:** none by that commit. But see below.
**Wrote:** First `test_forward_west_off_column_zero_lands_on_the_last_column`, which passed on its first run: Python's modulo already wraps negative `x`, as pong predicted. Kept it in the working tree as a Regression Test; it goes into the next green commit. Then `test_backward_facing_north_moves_one_row_south` — fails because `assert (2, 4) == (2, 2)`: `B` fell through to the forward branch.
**Interface decided:** none new.
**List:** checked the west wrap as "satisfied by 5c3e121, not driven"; checked the N case of `B`; split E, S, W backward into their own item.
**Surprise:** The west wrap was never driven by a test. It is behaviour the code had because of how Python's `%` treats negatives, not because anyone asked for it. That is exactly the "passing new test" case in the turn steps and it is a mild one: the code does more than its tests said, but what it does is right. Recorded rather than fixed.

## Turn 10 — pong

**Received:** `test_backward_facing_north_moves_one_row_south` failing because `assert (2, 4) == (2, 2)`: `B` fell through to the forward branch. Also the west-wrap regression test, uncommitted and passing.
**Green by:** Obvious Implementation — `B` applies the heading's step with the sign flipped.
**Refactored:** pulled the two move branches into one `_move(direction)` helper so F and B share the step lookup and the wrap.
**Commit:** d58031d (includes ping's west-wrap regression test)
**Also satisfied:** "`B` moves one square backward when heading E, S, or W" — B negates the same table F already covers for all four headings. Checked off as satisfied by d58031d, not driven.
**Wrote:** `test_right_turn_facing_north_ends_facing_east_without_moving` — fails because `assert 'N' == 'E'`: `R` is not `L` or `B`, so it fell through to a forward move; the position assert would also fail.
**Interface decided:** none new.
**List:** checked B for the other headings (satisfied, not driven); checked the N -> E case of `R`; split the other three right turns into their own item.
**Surprise:** none.

## Turn 11 — ping

**Received:** `test_right_turn_facing_north_ends_facing_east_without_moving` failing because `assert 'N' == 'E'`: `R` fell through to the forward move.
**Green by:** Obvious Implementation — a right-turn table with the one row the test needs, and a branch for `R`.
**Refactored:** nothing
**Commit:** 30068fa
**Also satisfied:** none
**Wrote:** `test_forward_into_an_obstacle_does_not_move_the_rover` — fails because `TypeError: Rover.__init__() got an unexpected keyword argument 'obstacles'`.
**Interface decided:** `Rover(..., obstacles=<set of (x, y) tuples>)`. This is the planet's map, handed in at creation so the rover can bump into things; it is not the rover's knowledge. Twist 2's discovered list will be a separate, initially empty, report.
**List:** split the obstacle item into three (does not move / abandons the rest / reports where) and checked the first.
**Surprise:** none. The split is the smallest test that makes an obstacle exist at all; the report format stays open for a later test.

## Turn 12 — pong

**Received:** `test_forward_into_an_obstacle_does_not_move_the_rover` failing because `TypeError: Rover.__init__() got an unexpected keyword argument 'obstacles'`.
**Green by:** Obvious Implementation — store the obstacle set; `_move` computes its target first and leaves the position alone when the target is an obstacle.
**Refactored:** nothing
**Commit:** bdf971e
**Also satisfied:** none
**Wrote:** `test_hitting_an_obstacle_abandons_the_rest_of_the_commands` — fails because `assert 'W' == 'N'`: the blocked `F` returned quietly and the loop went on to execute the `L`.
**Interface decided:** none new. `obstacles` defaults to empty so the earlier tests need no change.
**List:** checked "abandons the rest of the command string".
**Surprise:** none.

## Turn 13 — ping

**Received:** `test_hitting_an_obstacle_abandons_the_rest_of_the_commands` failing because `assert 'W' == 'N'`: the blocked move returned quietly and the loop carried on to the `L`.
**Green by:** Obvious Implementation — `_move` reports whether it moved; `execute` returns on the first move that did not.
**Refactored:** the F and B branches each repeated the "move, and stop if blocked" shape; replaced them with a `DIRECTION` table (`F` -> 1, `B` -> -1) and one branch.
**Commit:** 724615e
**Also satisfied:** none
**Wrote:** `test_rover_reports_the_obstacle_that_stopped_it` — fails because `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Interface decided:** `rover.blocked_by` is the `(x, y)` of the obstacle that stopped the last command string. What it holds when nothing stopped the rover is still on the list, not decided here.
**List:** checked "reports where the obstacle is".
**Surprise:** none.

## Turn 14 — pong

**Received:** `test_rover_reports_the_obstacle_that_stopped_it` failing because `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Green by:** Obvious Implementation — `_move` records the target it refused in `blocked_by`.
**Refactored:** nothing
**Commit:** 7fdb0fd
**Also satisfied:** none
**Wrote:** `test_rover_reports_no_obstacle_after_commands_that_hit_nothing` — fails because `AttributeError: 'Rover' object has no attribute 'blocked_by'`: the attribute only exists once a bump has set it.
**Interface decided:** `rover.blocked_by` is `None` when the last command string was not stopped by an obstacle.
**List:** checked "After a command string that hit nothing, the rover reports that it did not stop"; added "A command string that hits nothing clears the report of an earlier obstacle stop", because my test starts from a fresh rover and so does not settle that.
**Surprise:** none.

## Turn 15 — ping

**Received:** `test_rover_reports_no_obstacle_after_commands_that_hit_nothing` failing because `blocked_by` did not exist until a bump created it.
**Green by:** Obvious Implementation — `blocked_by` starts as `None` in the constructor.
**Refactored:** nothing
**Commit:** 97a9f9d
**Also satisfied:** none
**Wrote:** `test_commands_that_hit_nothing_clear_an_earlier_obstacle_report` — fails because `assert (2, 4) is None`: the report from the first string survives into the second. Used `R` as the second string so the rover does not need to move to prove the point.
**Interface decided:** none new; confirms `blocked_by` describes the last command string only.
**List:** checked the item pong added last turn.
**Surprise:** none.

## Turn 16 — pong

**Received:** `test_commands_that_hit_nothing_clear_an_earlier_obstacle_report` failing because `assert (2, 4) is None`: the report from the first string survived into the second.
**Green by:** Obvious Implementation — `execute` resets `blocked_by` to `None` before its loop.
**Refactored:** nothing
**Commit:** 2ad68e9
**Also satisfied:** none
**Wrote:** `test_forward_north_from_the_north_pole_row_crosses_the_pole` — fails because `assert (2, 6) == (7, 5)`: the rover walked off the top of the map; `height` has never been read. Width 10, so the far longitude of 2 is 7.
**Interface decided:** none new.
**List:** checked "Moving north from the north pole row ...".
**Surprise:** none. Chose the pole over the remaining turn-table rows because it is the first test that gives `height` a job and the first that changes heading during a move.

## Turn 17 — ping

**Received:** `test_forward_north_from_the_north_pole_row_crosses_the_pole` failing because `assert (2, 6) == (7, 5)`: `height` had never been read and the rover walked off the map.
**Green by:** Obvious Implementation — `_move` computes the raw target, and when its row equals `height` it folds back onto the top row, shifts longitude by half the width, and flips the heading through an `OPPOSITE` table. The table has one row because one test asks for one. Heading now changes inside `_move`, and only when the move is not blocked.
**Refactored:** nothing
**Commit:** cc18eb6
**Also satisfied:** none
**Wrote:** `test_backward_over_the_north_pole_flips_longitude_and_heading` — fails because `KeyError: 'S'` in `OPPOSITE`: the rover heading S backs up over the pole and there is no row saying what S flips to.
**Interface decided:** none new.
**List:** checked the north half of the backward-crossing item and split the south mirror into its own item.
**Surprise:** With the human's clarification, the pole rule is one sentence: any crossing shifts longitude by half the width and flips the heading, forward or backward alike. Without the clarification the backward case would have needed its own branch. The clarified rule is the simpler code.

## Turn 18 — pong

**Received:** `test_backward_over_the_north_pole_flips_longitude_and_heading` failing because `KeyError: 'S'` in `OPPOSITE`.
**Green by:** Obvious Implementation — the S -> N row in the opposite table.
**Refactored:** nothing
**Commit:** ba2619b
**Also satisfied:** none
**Wrote:** `test_forward_south_from_the_south_pole_row_crosses_the_pole` — fails because `assert (2, -1) == (7, 0)`: only the top edge is checked, so the rover walked off the bottom of the map.
**Interface decided:** none new.
**List:** checked "Moving south from the south pole row ...".
**Surprise:** none. The opposite table now has both rows the poles can ever need, since only N and S headings cross a pole.

## Turn 19 — ping

**Received:** `test_forward_south_from_the_south_pole_row_crosses_the_pole` failing because `assert (2, -1) == (7, 0)`: only the top edge was checked.
**Green by:** Obvious Implementation — a second branch for `y == -1`, a mirror of the first.
**Refactored:** the two edge branches were the same three lines with different constants. Replaced them with one: if the new row is off the map, undo the row step, shift longitude by half the width, flip the heading. The pole row the rover stays on falls out of undoing the step, so neither `height - 1` nor `0` appears in the code any more.
**Commit:** a9b6465
**Also satisfied:** none by that commit as such. But see below.
**Wrote:** First `test_backward_over_the_south_pole_flips_longitude_and_heading`, which passed on its first run: the unified crossing rule already covers it. Kept as a Regression Test in the working tree. Then `test_new_rover_has_discovered_no_obstacles` — fails because `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`.
**Interface decided:** `rover.discovered_obstacles` is a list of `(x, y)` tuples, in discovery order, empty on a new rover. The test gives the rover a planet with an obstacle so the empty list clearly means "not yet discovered" rather than "none exist".
**List:** checked the south backward crossing as "satisfied by a9b6465, not driven"; checked "A new rover reports no discovered obstacles". Twist 1 is now down to the obstacle-beyond-the-pole item.
**Surprise:** Three of the four pole crossings were driven by tests and the fourth came free from the refactor. The generalisation happened during Refactor, not Green: I had two branches that differed only in constants and folded them, and that fold is what made the fourth case pass. Textbook Beck, and a little eerie to watch.

## Turn 20 — pong

**Received:** `test_new_rover_has_discovered_no_obstacles` failing because `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`. Also ping's south-pole backward regression test, uncommitted and passing.
**Green by:** Obvious Implementation — an empty list in the constructor.
**Refactored:** nothing
**Commit:** 6896414 (includes the regression test)
**Also satisfied:** none
**Wrote:** `test_an_obstacle_the_rover_bumps_into_is_remembered` — fails because `assert [] == [(2, 4)]`: bumping records `blocked_by` but nothing is added to the discovered list.
**Interface decided:** none new.
**List:** checked "An obstacle the rover bumps into is remembered and reported".
**Surprise:** none.

## Turn 21 — ping

**Received:** `test_an_obstacle_the_rover_bumps_into_is_remembered` failing because `assert [] == [(2, 4)]`: the bump set `blocked_by` and nothing else.
**Green by:** Obvious Implementation — append the refused target to the discovered list.
**Refactored:** nothing
**Commit:** d5a0d78
**Also satisfied:** none
**Wrote:** `test_bumping_the_same_obstacle_again_does_not_record_it_twice` — fails because `assert [(2, 4), (2, 4)] == [(2, 4)]`: every bump appends.
**Interface decided:** none new.
**List:** checked "Bumping into the same obstacle again does not record it twice".
**Surprise:** This test is deliberately silent on whether the second `F` bumps or is refused as a known obstacle; either way the list must hold one entry. The refusal behaviour is still on the list for its own test.

## Turn 22 — pong

**Received:** `test_bumping_the_same_obstacle_again_does_not_record_it_twice` failing because `assert [(2, 4), (2, 4)] == [(2, 4)]`: every bump appended.
**Green by:** Obvious Implementation — append only when the target is not already in the list.
**Refactored:** nothing
**Commit:** 4c1f3e4
**Also satisfied:** none
**Wrote:** `test_commands_that_would_hit_a_known_obstacle_are_refused_without_moving` — fails because `assert (2, 4) == (2, 3)`: the rover took the first step of `FF` and only stopped on the bump. Setup: bump (2, 5) from (2, 4), back off to (2, 3), then ask for two steps north.
**Interface decided:** none new. The report of which known obstacle would have been hit is not asserted here.
**List:** split the refusal item; checked "does not move at all", added "A refused command string reports which known obstacle it would have hit" as its own item.
**Surprise:** none, though the setup needed three command strings before the assertion: the rover has to learn the obstacle, then step away from it, or "did not move at all" is indistinguishable from "stopped at the bump".

## Turn 23 — ping

**Received:** `test_commands_that_would_hit_a_known_obstacle_are_refused_without_moving` failing because `assert (2, 4) == (2, 3)`: the rover took the first step of `FF` and stopped on the bump.
**Green by:** Obvious Implementation — `execute` now walks the command string twice: first against the rover's own discovered obstacles, and if that walk would hit one, the string is refused and nothing changes; otherwise it walks for real against the planet. To make that possible the movement code became a pure `_walk(commands, obstacles)` over a pure `_step(position, heading, direction)`, neither of which touches rover state. The bookkeeping (report, discovered list) moved into `execute`.
**Refactored:** nothing beyond what the green needed; the restructuring above was the green.
**Commit:** 2e98644
**Also satisfied:** none by test. The dry run only turns on turns, so "Turning next to a known obstacle is not refused" is likely already true; left on the list for a test to find out.
**Wrote:** `test_refused_commands_report_the_known_obstacle_they_would_have_hit` — fails because `AttributeError: 'Rover' object has no attribute 'refused_by'`.
**Interface decided:** `rover.refused_by` is the `(x, y)` of the known obstacle that caused the last command string to be refused, separate from `blocked_by`, because the task describes them as different outcomes: one is a bump that stopped the rover part-way, the other is a plan the rover declined. What `refused_by` holds when nothing was refused is not settled by this test.
**List:** checked "A refused command string reports which known obstacle it would have hit".
**Surprise:** The refusal was the biggest step of the run so far and it did not fit inside the existing `_move`; the rover needed to be able to imagine a walk without taking it. Once movement was pure, the refusal was two lines. I did not plan for that shape; the test forced it.

## Turn 24 — pong

**Received:** `test_refused_commands_report_the_known_obstacle_they_would_have_hit` failing because `AttributeError: 'Rover' object has no attribute 'refused_by'`.
**Green by:** Obvious Implementation — `execute` keeps the dry run's result in `refused_by` instead of a local.
**Refactored:** nothing
**Commit:** 5fddb23
**Also satisfied:** none by test. Because `refused_by` is assigned from the dry run on every string, it is `None` whenever nothing was refused; nobody has asked for that yet, so it goes on the list.
**Wrote:** First tried `test_refused_commands_do_not_change_the_heading_either` with `LLBB`; it failed with `KeyError: 'W'` in the left-turn table, the wrong reason, so I withdrew it rather than hold two reds. Then `test_left_turn_facing_west_ends_facing_south` — fails because `KeyError: 'W'` in `LEFT`.
**Interface decided:** `rover.refused_by` mirrors `blocked_by`: the `(x, y)` of the known obstacle, set per command string.
**List:** checked the W -> S left turn; split S and E into their own item. Added "`refused_by` is `None` after a command string that was not refused".
**Surprise:** Most of what is left on the list looks like it already passes: ping's refusal green never touches state on refusal, the pole step runs before the obstacle check, and discovery appends in order. The remaining real reds are turn-table rows. I could not write the heading-unchanged test until the turns it needs exist.

## Turn 25 — ping

**Received:** `test_left_turn_facing_west_ends_facing_south` failing because `KeyError: 'W'` in `LEFT`.
**Green by:** Obvious Implementation — the W -> S row.
**Refactored:** nothing
**Commit:** e8600e4
**Also satisfied:** none
**Wrote:** `test_four_left_turns_pass_through_every_heading_and_return_to_north` — fails because `KeyError: 'S'` in `LEFT`. It records the heading after each of four `L`s and expects `W, S, E, N`, so it forces both remaining rows at once and shows the cycle closes.
**Interface decided:** none new.
**List:** checked the last left-turn item.
**Surprise:** none. Pong is right that most of what remains is likely already passing; the next turns will be mostly Regression Tests plus the right-turn rows.

## Turn 26 — pong

**Received:** `test_four_left_turns_pass_through_every_heading_and_return_to_north` failing because `KeyError: 'S'` in `LEFT`.
**Green by:** Obvious Implementation — the S -> E and E -> N rows.
**Refactored:** nothing. `RIGHT` is the inverse of `LEFT` and could be derived from it, but doing so would make the right-turn rows exist without a test, so I left that for after the right-turn test.
**Commit:** 9c63a80
**Also satisfied:** none
**Wrote:** `test_four_right_turns_pass_through_every_heading_and_return_to_north` — fails because `KeyError: 'E'` in `RIGHT`.
**Interface decided:** none new.
**List:** checked the last right-turn item.
**Surprise:** none.

## Turn 27 — ping

**Received:** `test_four_right_turns_pass_through_every_heading_and_return_to_north` failing because `KeyError: 'E'` in `RIGHT`.
**Green by:** Obvious Implementation — the three missing rows.
**Refactored:** `RIGHT` is now derived as the inverse of `LEFT`, which removes the second copy of the heading cycle. `OPPOSITE` could also be derived (two lefts) but it only has the two rows a pole can need, so I left it as a statement of fact.
**Commit:** 3b32a13
**Also satisfied:** none by that commit.
**Wrote:** Seven tests, one per remaining list item, and every one passed on its first run, so all are Regression Tests: turning beside an obstacle hits nothing; an obstacle on the far side of a pole stops the crossing; discovered obstacles come back in discovery order; a refused string leaves the heading alone; `refused_by` is `None` after an unrefused string; turning beside a known obstacle is not refused; an unknown obstacle is bumped, not refused. There is no next green to carry them, so I committed them together as a `test:` commit, fb63c54, on a green suite.
**Interface decided:** none new.
**List:** empty. Every item is checked, each marked as either test-driven, satisfied by a named commit, or a regression test.
**Surprise:** The last seven behaviours in the task cost no production code. The refusal green in turn 23 made movement a pure function of state and a map, and once that existed, "turning is fine either way", "unknown obstacles are bumped", and "refusal changes nothing" were not features but consequences. The test list was still worth keeping to the end: it is the record that each sentence of the task was checked against running code, and pong's prediction in turn 24 that they would pass was confirmed rather than assumed.

Baton: done. The human decides whether the list was finished.
