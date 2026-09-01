## Turn 1 — ping

**Received:** nothing — first turn of the run
**Green by:** n/a — no test existed to make pass
**Refactored:** nothing
**Commit:** 1995685 — scaffolding only (empty root `conftest.py`, empty `tests/`, the test list). No production code.
**Also satisfied:** none
**Wrote:** `test_new_rover_reports_the_position_and_heading_it_was_created_with` — fails at collection with `ModuleNotFoundError: No module named 'mars_rover'`
**Interface decided:** import name `mars_rover`; class `Rover`; constructed with keyword arguments `width`, `height`, `x`, `y`, `heading`; heading given as the string `"N"`; position and heading readable as `rover.x`, `rover.y`, `rover.heading`
**List:** wrote `.real-tdd/test-list.md` from the task (30 items). Checked off "created with a position and a heading" and "reports its position and heading". Added nothing.
**Surprise:** none
**Suite:** `.venv/bin/pytest` from the repository root (`.venv` is gitignored; `python3 -m venv .venv && .venv/bin/pip install pytest` rebuilds it)

## Turn 2 — pong

**Received:** `test_new_rover_reports_the_position_and_heading_it_was_created_with` failing at collection with `ModuleNotFoundError: No module named 'mars_rover'` — no production code existed yet.
**Green by:** Obvious Implementation — a class that keeps three values it was handed needs no faking. Created the package `mars_rover/` with `__init__.py` holding `Rover`. `width` and `height` are accepted by `__init__` and deliberately *not* stored: no test asks for them yet, and the list item for the grid is still open.
**Refactored:** nothing — one class, three assignments, no duplication to remove.
**Commit:** bd63320
**Also satisfied:** none
**Wrote:** `test_forward_moves_one_square_north_when_heading_north` — rover at (3, 2) heading N on a 10x6 grid, `execute("F")`, expects (3, 3, "N"). Fails with `AttributeError: 'Rover' object has no attribute 'execute'`.
**Interface decided:** the command string is run by a method named `execute`, taking the string as its single positional argument. Nothing decided about its return value — the assertion reads the position off the rover, as the starter test does.
**List:** checked off "`F` moves one square forward in the current heading" and "Moving north increases latitude". Added nothing.
**Surprise:** none. Worth recording though: y = 2 on a height-6 grid is two rows below the north pole row, chosen so this test says nothing about what happens at the edge. The pole items stay honestly untouched.
**Suite:** `.venv/bin/pytest` from the repository root — 1 passed, 1 failed.

## Turn 3 — ping

**Received:** `test_forward_moves_one_square_north_when_heading_north` failing with `AttributeError: 'Rover' object has no attribute 'execute'`
**Green by:** Obvious Implementation — `execute` walks the command string one character at a time and `F` does `self.y += 1`. The loop is obvious; the direction is deliberately left un-generalized, since one north-facing test cannot demand that the heading be consulted.
**Refactored:** nothing. The two tests share a construction line, but at two occurrences extracting it would cost more in Evident Data than it saves.
**Commit:** 89cb8d1
**Also satisfied:** none
**Wrote:** `test_forward_moves_one_square_east_when_heading_east` — rover at (3, 2) heading E, `execute("F")`, expects (4, 2, "E"). Fails with `assert (3, 3, 'E') == (4, 2, 'E')`: forward still steps north regardless of heading.
**Interface decided:** none — same constructor and `execute` as before, only `heading="E"` is new.
**List:** checked off "Moving east increases longitude". Added nothing.
**Surprise:** none. This is Triangulate on the heading axis: N and E are the two examples that make consulting `self.heading` unavoidable. A second north-facing example would not have forced it.

## Turn 4 — pong

**Received:** `test_forward_moves_one_square_east_when_heading_east` failing with `assert (3, 3, 'E') == (4, 2, 'E')` — forward stepped north while the rover faced east, because `execute` never consulted `self.heading`.
**Green by:** Triangulate — the north and east examples together rule out a fixed step, so `F` became a lookup of a unit step keyed by heading. The table holds only `"N"` and `"E"`; south and west are not in it, because no test asks what forward means facing those ways. A `KeyError` is what a rover facing south would get today, and that is the honest state of the code.
**Refactored:** nothing separate. The generalization *was* the removal of the duplication between the tests' expected coordinates and the hard-coded `self.y += 1`, so it happened inside the green step.
**Commit:** 3cdf2cd
**Also satisfied:** none
**Wrote:** `test_left_turns_the_rover_from_north_to_west` — rover at (3, 2) heading N, `execute("L")`, expects (3, 2, "W"). Fails with `assert (3, 2, 'N') == (3, 2, 'W')`: `L` is currently ignored by the command loop, so the heading never changes.
**Interface decided:** none — turning goes through the same `execute` string, and the heading is still read off `rover.heading` as a one-letter string. No separate turn method.
**List:** checked off "`L` turns left ninety degrees". Added two items the green step exposed: "`F` while heading south moves one square south" and "`F` while heading west moves one square west" — the two entries missing from the step table.
**Surprise:** the position half of the new test's assertion is doing real work. `(3, 2, "W")` also says a turn moves nothing, which is the first thing written down about turning being different in kind from moving — the list item "Turning never hits anything" is the far end of the same fact.
**Suite:** `.venv/bin/pytest` from the repository root — 3 passed, 1 failed.

## Turn 5 — ping

**Received:** `test_left_turns_the_rover_from_north_to_west` failing with `assert (3, 2, 'N') == (3, 2, 'W')` — the command loop had no branch for `L`, so the heading was untouched.
**Green by:** Fake It, in table form — `_LEFT_TURN = {"N": "W"}`, one entry, which is the test's expected value moved into the code. I know the real implementation (headings are a cycle and a turn is a step around it), but one example cannot demand it, so the constant stays visible where a second example will force it out.
**Refactored:** nothing. `_FORWARD_STEP` and `_LEFT_TURN` are both partial tables keyed by heading, which looks like duplication but is not yet: they map to different things and neither is complete.
**Commit:** 5c85fef
**Also satisfied:** none
**Wrote:** `test_right_turns_the_rover_from_north_to_east` — rover at (3, 2) heading N, `execute("R")`, expects (3, 2, "E"). Fails with `assert (3, 2, 'N') == (3, 2, 'E')`: `R` is ignored by the command loop.
**Interface decided:** none.
**List:** checked off "`R` turns right ninety degrees". Added nothing.
**Surprise:** none, but a choice worth recording. `execute("FF")` would have been the obvious next item ("a command string is executed in order") and it would have passed on the spot — the loop already does it. That would have been a Regression Test, not a step, so I picked `R` instead and left the sequencing item for a test that can actually go red.

## Turn 6 — pong

**Received:** `test_right_turns_the_rover_from_north_to_east` failing with `assert (3, 2, 'N') == (3, 2, 'E')` — the command loop had no branch for `R`.
**Green by:** Obvious Implementation — I could see the abstraction, so Triangulate would have been the slow road. `_LEFT_TURN = {"N": "W"}` and the `_RIGHT_TURN = {"N": "E"}` I would have written to fake this are the same fact read in opposite directions, so both became `_CLOCKWISE = ("N", "E", "S", "W")` and a signed step around it: `L` is -1, `R` is +1. Stated plainly: this generalizes past the two examples on the list — the code now answers E -> S with no test asking. That is what Obvious Implementation costs, and I took it knowingly rather than write a second one-entry table.
**Refactored:** nothing after the fact; the duplication between the two turn tables was removed as part of getting green, which is where seeing the abstraction puts it.
**Commit:** 618cfa1
**Also satisfied:** none as behavior the list names. `_CLOCKWISE` is a complete ordering of all four headings while `_FORWARD_STEP` still knows only two, so the two south/west forward items stay open and honest.
**Wrote:** `test_moving_east_off_the_last_column_wraps_to_column_zero` — rover at (9, 2) heading E on a width-10 grid, `execute("F")`, expects (0, 2, "E"). Fails with `assert (10, 2, 'E') == (0, 2, 'E')`: the rover walks off the edge of the map.
**Interface decided:** none new. The test does put weight on an argument that has been inert since turn 2 — this is the first test whose expected value depends on `width`.
**List:** checked off "Longitude wraps: moving east off the last column lands on column 0". Added nothing.
**Surprise:** the turn tests are where the heading cycle came from, but the cycle is also the whole of Twist 1's answer waiting to be used — crossing a pole is "keep the row, add half a width, and turn twice". I did not write that anywhere in the code and there is no test for it; noting it because the journal is the data, not because the next turn should act on it.
**Suite:** `.venv/bin/pytest` from the repository root — 5 passed, 1 failed.

## Turn 7 — ping

**Received:** `test_moving_east_off_the_last_column_wraps_to_column_zero` failing with `assert (10, 2, 'E') == (0, 2, 'E')` — the column was never bounded, so the rover walked off the map. `width` had been accepted and discarded since turn 2.
**Green by:** Obvious Implementation — the rover now keeps `self.width` and the forward step does `self.x = (self.x + step_x) % self.width`. Modulo is what "longitude wraps" means; faking it with `if self.x == self.width: self.x = 0` would have been a constant I could not defend.
**Refactored:** nothing. `self.y += step_y` is now visibly asymmetric with the wrapped `x`, and that asymmetry is correct rather than untidy: Twist 1 says latitude does not wrap. Leaving it uneven is the code telling the truth about the sphere.
**Commit:** 1222798
**Also satisfied:** "Longitude wraps the other way: moving west off column 0 lands on the last column" — checked off on the list as satisfied by 1222798, not driven. Python's modulo makes `(0 - 1) % 10` come out 9, so the reverse direction fell out of the same expression. No test asserts it.
**Wrote:** `test_backward_moves_one_square_south_when_heading_north` — rover at (3, 2) heading N, `execute("B")`, expects (3, 1, "N"). Fails with `assert (3, 2, 'N') == (3, 1, 'N')`: the command loop ignores `B`.
**Interface decided:** none.
**List:** checked off "`B` moves one square backward"; checked off the west-wrap item as satisfied-not-driven (above). Added nothing.
**Surprise:** how much the step table still does not know. `B` while heading north wants the south step, and `_FORWARD_STEP` has no `"S"` entry — so the smallest honest green is negating a step rather than looking one up, and the two open south/west forward items survive a turn that walks the rover south.

## Turn 8 — pong

**Received:** `test_backward_moves_one_square_south_when_heading_north` failing with `assert (3, 2, 'N') == (3, 1, 'N')` — no `B` branch in the command loop.
**Green by:** Obvious Implementation — with `_FORWARD_STEP` still holding only north and east, looking up a backward step was not available; negating the forward one was. `B` got its own branch with `- step_x` and `-= step_y`.
**Refactored:** the `F` and `B` branches, which after the green differed only in a sign. Both became `self._move(1)` and `self._move(-1)` over a `_move(squares_forward)` that scales the step. That leaves the class with two signed operations, `_move` and `_turn`, which is the first time the shape of the thing has looked deliberate rather than accumulated. Suite green after the extraction.
**Commit:** fd2864c
**Also satisfied:** none
**Wrote:** `test_forward_moves_one_square_south_when_heading_south` — rover at (3, 2) heading S on a 10x6 grid, `execute("F")`, expects (3, 1, "S"). Fails with `KeyError: 'S'` raised inside `_move`.
**Interface decided:** none.
**List:** checked off "`F` while heading south moves one square south". Added nothing.
**Surprise:** the red is a `KeyError` from production code rather than a failed assertion, and that is the honest shape of this gap — the rover cannot answer the question at all, rather than answering it wrongly. It is the bill for turn 6, where `_CLOCKWISE` learned all four headings and `_FORWARD_STEP` was left knowing two. A rover that turns right twice and then moves forward has been able to crash since then; no test caught it, because the item that names it was on the list unchecked, which is exactly where the list is supposed to hold a behavior that has no test.
**Suite:** `.venv/bin/pytest` from the repository root — 7 passed, 1 failed.

## Turn 9 — ping

**Received:** `test_forward_moves_one_square_south_when_heading_south` failing with `KeyError: 'S'` from `_move`.
**Green by:** Obvious Implementation — one entry, `"S": (0, -1)`. There was nothing to fake: the table already existed and the missing row is the whole of the behavior. I did not add `"W"` at the same time; no test asks for it.
**Refactored:** nothing. `_FORWARD_STEP`'s keys and `_CLOCKWISE`'s members are visibly the same four headings written twice, which is duplication — but it cannot be removed while the table is missing a row, since deriving one from the other would hand the rover a west step no test demands. Recording it as seen and deliberately left.
**Commit:** ed10049
**Also satisfied:** none
**Wrote:** `test_forward_moves_one_square_west_when_heading_west` — rover at (3, 2) heading W, `execute("F")`, expects (2, 2, "W"). Fails with `KeyError: 'W'` from `_move`.
**Interface decided:** none.
**List:** checked off "`F` while heading west moves one square west". Added nothing.
**Surprise:** none, and the flatness is the point of writing it down. This is the least interesting test of the run — a fourth example on an axis already generalized — and it exists only because turn 6's Obvious Implementation generalized the turn cycle past the step table and left a hole. The dull test is the invoice for the clever green.

## Turn 10 — pong

**Received:** `test_forward_moves_one_square_west_when_heading_west` failing with `KeyError: 'W'` from `_move`.
**Green by:** Obvious Implementation — the fourth row, `"W": (-1, 0)`. Nothing else was available; the missing row was the whole behavior.
**Refactored:** the duplication turn 9 saw and left. With the table finally holding all four headings, `_CLOCKWISE` no longer needs to name them a second time: the table is written in clockwise order and the cycle is `tuple(_FORWARD_STEP)`. That trades a repetition for an ordering the table is now obliged to keep, so the obligation is written above it in a comment — the only comment in the production code, and it is there because the constraint is invisible otherwise. Suite green after the change.
**Commit:** 0d3c39f
**Also satisfied:** none
**Wrote:** `test_forward_off_the_north_pole_row_crosses_the_pole_heading_south` — rover at (3, 5) heading N on a 10x6 grid, so it is standing on the north pole row; `execute("F")` expects (8, 5, "S"). Fails with `assert (3, 6, 'N') == (8, 5, 'S')`: the rover walks off the top of the map into row 6, which does not exist.
**Interface decided:** none new, but `height` finally matters. It has been accepted and discarded since turn 2 and this is the first expected value that depends on it.
**List:** checked off "Moving north off the north pole row leaves the rover on the north pole row, at longitude `x + width / 2` modulo `width`, heading south" and, with it, "Moving north off the north pole row does not wrap to the south pole row" — the failure `(3, 6, ...)` is that item's content, and a test asserting only "not row 0" would assert a negative and pass for the wrong reason. Also checked off "The rover is created with a rectangular grid `width` columns by `height` rows", now driven, and "A command string is executed in order" (see below).
**Regression test in the tree:** `test_a_command_string_is_executed_one_command_after_another` — `execute("FFRFF")` from (3, 2) heading N expects (5, 4, "E"). It passed the moment it was written; the command loop has done this since turn 3 with nothing asserting it. Not a step, and not committed on its own: it is uncommitted in the working tree and belongs in the next green commit alongside the pole.
**Surprise:** the pole test needed no new interface at all. Every twist so far has been payable in the vocabulary the classic part already fixed — a position, a heading, a command string — which is why the task could be silent about the interface and still be unambiguous. Whether that holds for Twist 2 is the open question: "ask the rover what it has discovered" is the first item on the list that no existing method can answer.
**Suite:** `.venv/bin/pytest` from the repository root — 10 passed, 1 failed.

## Turn 11 — ping

**Received:** `test_forward_off_the_north_pole_row_crosses_the_pole_heading_south` failing with `assert (3, 6, 'N') == (8, 5, 'S')` — the rover stepped into row 6 on a six-row map. Also received `test_a_command_string_is_executed_one_command_after_another` as an uncommitted regression test; it went into this turn's commit as the journal said it should.
**Green by:** Obvious Implementation — the rover keeps `self.height`, and `_move` computes the destination before storing it. If the new row is past the north pole row, the rover stays on that row, takes `x + width // 2` modulo width, and `self._turn(2)` reverses the heading. Turning twice rather than assigning `"S"` is the point: the pole crossing borrows the cycle that turn 6's green built, which is why this behavior needed no new vocabulary.
**Refactored:** nothing. The pole branch is a special case sitting inside `_move`, which is where the sphere actually differs from the torus; hiding it would not make the map rounder.
**Commit:** 2a757be
**Also satisfied:** none. The south pole is untouched — the branch tests one end of the axis only.
**Wrote:** `test_forward_off_the_south_pole_row_crosses_the_pole_heading_north` — rover at (3, 0) heading S, `execute("F")`, expects (8, 0, "N"). Fails with `assert (3, -1, 'S') == (8, 0, 'N')`: the rover steps to row -1, off the bottom of the map, because the branch only looks upward.
**Interface decided:** none.
**List:** checked off "Moving south off the south pole row leaves the rover on the south pole row...". Added nothing.
**Surprise:** `_move` splitting into "work out where this lands" and "go there" was forced by the pole and not by me. Until this turn the rover mutated `self.x` and `self.y` in place; a crossing has to know the destination before it can decide the destination is wrong, so the local `x` and `y` appeared. The obstacle items on the list need exactly the same shape — look before you leap — and it arrived on the sphere's account, a turn before anything asks for it.

## Turn 12 — pong

**Received:** `test_forward_off_the_south_pole_row_crosses_the_pole_heading_north` failing with `assert (3, -1, 'S') == (8, 0, 'N')` — the crossing branch only looked upward, so the rover stepped to row -1.
**Green by:** Triangulate — north and south are the two ends of one axis, which is exactly the pair that forces the generalization. `if y > self.height - 1` became `if not 0 <= y < self.height`: the question is no longer "did it go too far north" but "did it leave the map at all". The row it lands on became `self.y`, because a move is one square, so a rover that just left the map was standing on the pole row it must stay on. That also removed the last duplication between the test's `5` and a `height - 1` in the code.
**Refactored:** nothing after the fact; the generalization was the whole green.
**Commit:** 1dbbb6c
**Also satisfied:** none
**Wrote:** `test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was` — rover at (3, 2) heading N with an obstacle on (3, 3), `execute("F")`, expects (3, 2, "N"). Fails with `TypeError: Rover.__init__() got an unexpected keyword argument 'obstacles'`.
**Interface decided:** obstacles reach the rover as a constructor keyword `obstacles`, holding `(x, y)` pairs. Two things follow that I chose deliberately. It has to have a default, because thirteen existing tests construct a rover without it. And it is the world's truth, not the rover's map — Twist 2 says the rover is not told where the obstacles are, so this argument must never be readable as the answer to "what has the rover discovered"; that will be a separate thing with a separate name. The alternative was a `Planet` object owning `width`, `height` and `obstacles`, which is where this may end up, but nothing yet duplicates enough to force it.
**List:** checked off "A move that would land on an obstacle does not happen: the rover does not move", and "A backward move crosses the pole the way a forward move in the opposite heading would" (see below).
**Regression test in the tree:** `test_backward_off_the_north_pole_row_crosses_the_pole_like_a_forward_move` — rover on the north pole row heading S, `execute("B")`, expects (8, 5, "N"). I wrote it expecting red and it passed, so it is a regression test, not a step; uncommitted, for the next green commit. It passes because `_move` scales the step by the sign rather than branching on the command, which turn 8's refactoring did for tidiness and which turns out to have been the whole of this list item.
**Surprise:** two list items in a row have turned out to be already true. Both were paid for by refactorings done for other reasons — the signed `_move` in turn 8, the destination locals in turn 11. The list is measuring something real here: it holds behaviors the task asks for, and the gap between "the task asks for it" and "a test demands it" is where code written for tidiness quietly lands. Neither was a bug, but neither was verified either, until the list made someone go and look.
**Suite:** `.venv/bin/pytest` from the repository root — 13 passed, 1 failed.

## Turn 13 — ping

**Received:** `test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was` failing with `TypeError: Rover.__init__() got an unexpected keyword argument 'obstacles'`. Also received `test_backward_off_the_north_pole_row_crosses_the_pole_like_a_forward_move` as an uncommitted regression test; it went into this turn's commit.
**Green by:** Obvious Implementation — `obstacles=()` on the constructor, stored as handed over, and `_move` returns without storing the destination when `(x, y)` is in it. Turn 11's destination locals were already there, so the check had somewhere to stand.
**Refactored:** nothing, and I want to record what I chose not to do. The obstacle check sits *after* the pole branch, and that branch has already called `self._turn(2)` by then — so a rover blocked by an obstacle on the far side of a pole would today keep the turn while refusing the move. The fix is to make `_turn` pure and commit the heading with the position, and I did not do it: no test demands it, so under refactoring rules it would be adding behavior. The list item "An obstacle on the far side of the pole stops the pole crossing like any other obstacle" is where that behavior lives until a test asks for it. Flagging it here rather than fixing it quietly.
**Commit:** 3c842b9
**Also satisfied:** none
**Wrote:** `test_a_move_onto_an_obstacle_abandons_the_rest_of_the_command_string` — rover at (3, 2) heading N, obstacle on (3, 3), `execute("FR")`, expects (3, 2, "N"). Fails with `assert (3, 2, 'E') == (3, 2, 'N')`: the blocked `F` is skipped but the `R` after it still turns.
**Interface decided:** none new. The test reuses pong's `obstacles` keyword unchanged.
**List:** checked off "A move that would land on an obstacle abandons the rest of the command string". Added nothing.
**Surprise:** the failure reads `'E' != 'N'` — a turn, not a position. The cheapest green for the previous test was a `return` inside `_move`, which stops one move and nothing else, so the evidence that the command string kept running shows up in the heading. That is the same crack as the pole-turn hazard above: the rover has two ways to say "did not move" and only one of them stops the string.

## Turn 14 — pong

**Received:** `test_a_move_onto_an_obstacle_abandons_the_rest_of_the_command_string` failing with `assert (3, 2, 'E') == (3, 2, 'N')` — the blocked `F` was skipped but the `R` after it still turned, because a bare `return` inside `_move` was invisible to the loop that called it.
**Green by:** Obvious Implementation — `_move` now answers whether it moved, and `execute` breaks when it did not. There was nothing to fake: the missing thing was a channel from the move back to the loop, and a return value is that channel.
**Refactored:** the command dispatch. With `if not self._move(...): break` written once for `F` and once for `B`, the four-branch `if`/`elif` chain was mostly repetition of the two arguments that actually differ, so the commands became `_SQUARES_FORWARD = {"F": 1, "B": -1}` and `_QUARTER_TURNS_CLOCKWISE = {"L": -1, "R": 1}`, in the style of the step table already in the class. The `break` is now written once. Unknown command characters are still ignored, as before — that is untested either way, so preserving it was deliberate rather than incidental. Suite green after the change.
**Commit:** ac550ed
**Also satisfied:** none
**Wrote:** `test_after_hitting_an_obstacle_the_rover_reports_which_obstacle_it_was` — rover at (3, 2) heading N, obstacle on (3, 3), `execute("F")`, expects `rover.blocked_by == (3, 3)`. Fails with `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Interface decided:** the obstacle report is an attribute, `rover.blocked_by`, holding the `(x, y)` of the obstacle that stopped the run. That follows the shape every test has used since turn 1 — ask the rover, do not read a return value — and it keeps `execute` returning nothing, which matters because the same string can end four ways before this is done (ran out, bumped, refused, ran clean) and an attribute can carry all of them. The name says "blocked", not "hit", because Twist 2's refusal is the same question asked before the fact. What it holds after a clean run is *not* decided by this test; the list item for that is still open and is the next test's business, not this one's.
**List:** checked off "After hitting an obstacle the rover reports that it stopped because of an obstacle, and which one". Added nothing.
**Surprise:** none this turn, but the refactoring quietly answered a question the list has been holding since turn 1. "Turning never hits anything" is now structural rather than incidental: turns are dispatched down a branch that cannot consult `obstacles` and cannot `break`. The item stays open because no test says so, and a test would pass on the spot — but it is worth recording that the reason changed from "nobody wrote that code" to "the code is shaped so it cannot".
**Suite:** `.venv/bin/pytest` from the repository root — 15 passed, 1 failed.

## Turn 15 — ping

**Received:** `test_after_hitting_an_obstacle_the_rover_reports_which_obstacle_it_was` failing with `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Green by:** Obvious Implementation — one line where the block is already detected: `self.blocked_by = (x, y)` beside the `return False`. I did not initialise it in `__init__`, though the missing attribute is conspicuous. Setting it to `None` there would have been code deciding what a rover that has hit nothing reports, which is the item still open on the list, so I left the attribute conditional and ugly rather than answer an unasked question in the constructor.
**Refactored:** nothing.
**Commit:** a3a2987
**Also satisfied:** none
**Wrote:** `test_after_a_command_string_that_hits_nothing_the_rover_reports_no_obstacle` — rover at (3, 2) heading N, obstacle on (3, 3), bumps it with `execute("F")`, then `execute("RF")` runs clean to (4, 2). Expects `(rover.x, rover.y, rover.blocked_by) == (4, 2, None)`. Fails with `(4, 2, (3, 3)) != (4, 2, None)`: the report from the previous string is still standing.
**Interface decided:** `blocked_by` is `None` when the last command string was not stopped by an obstacle. That is the "whether it stopped" half of the task's report sentence; the task leaves the encoding to us and `None` against a coordinate pair is the plainest reading.
**List:** checked off "After a command string with no obstacle the rover reports that it did not stop because of an obstacle". Added nothing.
**Surprise:** the test went red for the interesting reason rather than the boring one. A fresh rover asked for `blocked_by` was also red — `AttributeError` — and that was the cheaper test to write. Making the rover bump first and *then* run clean turns the assertion into one about staleness, which is a real behavior, where the fresh-rover version would only have demanded an initialiser. The position in the assertion is doing work too: without it the test passes on a rover that refused to move at all.

## Turn 16 — pong

**Received:** `test_after_a_command_string_that_hits_nothing_the_rover_reports_no_obstacle` failing with `(4, 2, (3, 3)) != (4, 2, None)` — the report from the earlier bump was still standing after a clean run.
**Green by:** Obvious Implementation — `execute` clears `self.blocked_by` before running the string. The report belongs to the last command string, and that is where a command string starts.
**Refactored:** nothing.
**Commit:** 396cdff
**Also satisfied:** none. The rover that has never run a command string still has no `blocked_by` at all — clearing it inside `execute` does not reach the constructor. Turn 15 left that unanswered on purpose and it is still unanswered; I have put it on the list rather than fix it, marked as not something the task asks for, because the task's report sentence begins "after any command string".
**Wrote:** `test_an_obstacle_across_the_pole_stops_the_crossing_and_the_rover_stays_put` — rover at (3, 5) heading N on a 10x6 grid with an obstacle on (8, 5), the square across the north pole; `execute("F")` expects (3, 5, "N") and `blocked_by == (8, 5)`. Fails with `assert (3, 5, 'S', (8, 5)) == (3, 5, 'N', (8, 5))`: the rover is stopped and reports correctly, but it kept the pole turn.
**Interface decided:** none. The test asserts the defect turn 13 flagged and left: `_turn(2)` mutates the heading inside `_move` before the obstacle check can refuse the move. I read the task's "the rover does not move" as covering the whole move, heading included, since across a pole the turn *is* part of the move rather than a separate `L` or `R`. That reading is not something the task spells out, but it is the same one turn 13's journal entry named when it flagged the crack, so both sessions arrived at it independently and I did not stop to ask.
**List:** checked off "An obstacle on the far side of the pole stops the pole crossing like any other obstacle", and "Turning never hits anything" (see below). Added "A rover that has not run a command string yet reports no obstacle", flagged as beyond the task.
**Regression test in the tree:** `test_turning_never_hits_an_obstacle` — a rover with obstacles on all four neighbouring squares runs `execute("LLRR")` and comes back to (3, 2, "N") with no report. It passed as written. Turn 14's dispatch refactoring is what makes it structural: turns go down a branch that cannot reach `obstacles` and cannot `break`.
**Surprise:** the two tests in this turn's tree disagree about what a turn is, and both are right. `test_turning_never_hits_an_obstacle` says a turn cannot be blocked; the pole test says a turn can be undone by a block. They are consistent only because the pole turn is not a command — it is part of executing `F`. That distinction has been implicit in the code since turn 11 and nothing named it until two tests sat next to each other and looked contradictory.
**Suite:** `.venv/bin/pytest` from the repository root — 18 passed, 1 failed.

## Turn 17 — ping

**Received:** `test_an_obstacle_across_the_pole_stops_the_crossing_and_the_rover_stays_put` failing with `assert (3, 5, 'S', (8, 5)) == (3, 5, 'N', (8, 5))` — the defect turn 13 saw and left, now with a test on it. Also received `test_turning_never_hits_an_obstacle` as an uncommitted regression test; it went into this turn's commit.
**Green by:** Obvious Implementation — the heading joined the destination. `_move` now keeps a local `heading` alongside the local `x` and `y`, and all three are stored together only if the move happens. That needed `_turn` split into the mutation and a pure `_turned(heading, quarter_turns)` the pole branch can call without committing to it. Turn 11 wrote "a crossing has to know the destination before it can decide the destination is wrong"; the heading turned out to be part of the destination, which is the part that entry missed.
**Refactored:** nothing after the fact. Splitting `_turn` was inside the green, because without it there was no way to reach the behavior the test asked for.
**Commit:** c264799
**Also satisfied:** none
**Wrote:** `test_a_new_rover_has_discovered_no_obstacles` — a rover created with an obstacle in the world it has not met, asserting `rover.discovered_obstacles == ()`. Fails with `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`.
**Interface decided:** `rover.discovered_obstacles`, an attribute holding a tuple of `(x, y)` pairs. An attribute because every report the rover makes is one, a tuple because the task asks for them "in the order it discovered them" and a tuple is ordered and cannot be edited by whoever reads it. The name is deliberately not `obstacles`: the constructor keyword of that name is the world's truth, and the rover must not be able to read the answer out of it.
**List:** checked off "The rover starts with no map: asked for discovered obstacles before it moves, it has none". Added nothing.
**Surprise:** the test gives the rover an obstacle at (3, 3) and then asserts the rover knows nothing about it. That construction looks pointless — an empty world would fail the same way today — but it is the only test in the suite where the world and the rover's belief are deliberately different, and it is the one assertion that would catch a green that satisfies the item by handing back `self.obstacles`.

## Turn 18 — pong

**Received:** `test_a_new_rover_has_discovered_no_obstacles` failing with `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`.
**Green by:** Obvious Implementation — one line in the constructor, `self.discovered_obstacles = ()`. Worth saying why it went there rather than beside `blocked_by`'s lazy creation: the task says the rover can be asked "at any time", so unlike the obstacle report this one has to exist before the first command string. The two attributes look alike and are not.
**Refactored:** nothing.
**Commit:** 6566aee
**Also satisfied:** none as a list item, but the empty tuple sitting next to `self.obstacles` in the constructor is now the whole of Twist 2's premise written down in two lines — what the world contains, and what the rover has found out. Nothing yet moves anything from the first to the second.
**Wrote:** `test_bumping_into_an_unknown_obstacle_discovers_it` — rover at (3, 2) heading N with an obstacle on (3, 3), `execute("F")`, expects `rover.discovered_obstacles == ((3, 3),)`. Fails with the tuple still empty: "Right contains one more item: (3, 3)".
**Interface decided:** none new. The test reuses `discovered_obstacles` as turn 17 fixed it and asserts on a one-element tuple, which pins that discoveries accumulate in a sequence rather than a set — the ordering item is next on the list and a set would already have made it unreachable.
**List:** checked off "An obstacle the rover has not discovered is discovered the classic way: the rover moves up to it, bumps, stops, and learns it". Added nothing.
**Surprise:** how little there is left to build. `_move` already computes the obstacle and already writes it to `blocked_by`; this test asks for the same value to be written to a second place. The three remaining discovery items — order, no duplicates, and the whole refusal — will all be paid for out of that one line, and only the refusal needs `execute` to learn anything new. Turn 12 guessed that Twist 2 would need vocabulary the classic part had not fixed; so far the only new word is the name of the list itself.
**Suite:** `.venv/bin/pytest` from the repository root — 20 passed, 1 failed.

## Turn 19 — ping

**Received:** `test_bumping_into_an_unknown_obstacle_discovers_it` failing with `assert () == ((3, 3),)` — the discovered map was created empty in turn 18 and nothing ever added to it.
**Green by:** Obvious Implementation — `self.discovered_obstacles += ((x, y),)` beside the `blocked_by` line that already had the square in hand.
**Refactored:** nothing. Two consecutive lines now write the same value to two attributes, which reads like duplication and is not: one is "what stopped this command string" and is cleared at the start of the next, the other is "what this rover knows" and is not. Same value, different lifetimes.
**Commit:** 1a44d52
**Also satisfied:** none
**Wrote:** `test_bumping_into_the_same_obstacle_twice_records_it_once` — rover at (3, 2) heading N, obstacle on (3, 3), `execute("F")` twice. Expects `((3, 3),)`, fails with `((3, 3), (3, 3))`.
**Interface decided:** none.
**List:** checked off "Bumping into the same obstacle again does not record it twice". Also checked off "The rover can be asked at any time for the obstacles it has discovered" — not driven by a new test, but demonstrated by two that exist: turn 17's asks before the rover has moved, turn 18's asks after a bump, which is what "at any time" says. Added nothing.
**Surprise:** this test can only be red today, and it is why I wrote it now instead of the ordering item. Once "a command string that would hit a known obstacle is refused as a whole" lands, the second `execute("F")` here will be refused before it moves — so the rover will never bump a known obstacle again, and the no-duplicates rule becomes unreachable through `execute`. The test will keep passing for a reason that has nothing to do with its name. Both sentences are in the task and they do not contradict each other; the second just makes the first unobservable from outside. Writing it now is the only chance to see it fail, and after the refusal lands this test is a monument rather than a check.

## Turn 20 — pong

**Received:** `test_bumping_into_the_same_obstacle_twice_records_it_once` failing with `((3, 3), (3, 3)) == ((3, 3),)`.
**Green by:** Obvious Implementation — guard the append with `not in`. Nothing to fake; the rule is the guard.
**Refactored:** two things. The square the move lands on was written out as `(x, y)` four times inside that block and is now `destination`, named before the check that decides what it is. And the no-duplicates rule moved into `_discover(obstacle)`, where the argument can honestly be called an obstacle because it only gets there having been one. `_move` is the longest thing in the class and this is the second time the way to shorten it has been to name a rule rather than to split the method. Suite green after each change.
**Commit:** 6b0ede4
**Also satisfied:** none
**Wrote:** `test_a_command_string_that_would_hit_a_known_obstacle_is_refused_before_it_moves` — the rover bumps (3, 3) to learn it, backs off to (3, 1), then runs `execute("FF")`, whose first `F` is legal and whose second would hit the known obstacle. Expects (3, 1, "N"). Fails with `assert (3, 2, 'N') == (3, 1, 'N')`: the rover took the legal step before stopping.
**Interface decided:** none. Getting the rover to (3, 1) took two setup command strings rather than one, and that is not clumsiness: a string is abandoned at a bump, so the rover cannot learn an obstacle and reposition in the same breath. The test's shape is a consequence of the behavior turn 14 built.
**List:** checked off "Bumping into the same obstacle again does not record it twice", "A command string that would bump into an obstacle the rover already knows about is refused as a whole", and "Discovered obstacles come back in the order they were discovered" (see below).
**Regression test in the tree:** `test_discovered_obstacles_come_back_in_the_order_they_were_discovered` — the rover bumps (4, 2) heading east, turns north and bumps (3, 3), and the tuple comes back in that order. It passed as written, because a tuple appended to is ordered by construction. The two squares are chosen so that discovery order is not also their sorted order; with obstacles discovered north-then-east the assertion would have passed against a sorted or an arbitrary implementation and proved nothing.
**Surprise:** the refusal test is the first one in the run whose *setup* is three command strings rather than a constructor. Every test until now could state its precondition by building a rover in that state, because everything the rover knew, it was told. What the rover has learned cannot be handed to the constructor — Twist 2 says so — and so the only way to arrange a rover that knows something is to make it go and find out. The twist is enforced by the tests being awkward to write, not by anything in the code.
**Suite:** `.venv/bin/pytest` from the repository root — 23 passed, 1 failed.

## Turn 21 — ping

**Received:** `test_a_command_string_that_would_hit_a_known_obstacle_is_refused_before_it_moves` failing with `assert (3, 2, 'N') == (3, 1, 'N')` — the rover took the legal first step before stopping. Also received `test_discovered_obstacles_come_back_in_the_order_they_were_discovered` as an uncommitted regression test; it went into this turn's commit.
**Green by:** Obvious Implementation — walk the string against `discovered_obstacles` first and return without touching anything if that walk is stopped. To walk it at all, `_move` had to give up its destination as a value, so `_destination(x, y, heading, squares_forward)` came out of it, pure, taking the state to work from rather than reading `self`.
**Refactored:** the duplication the green created, which was the whole command loop written twice — once mutating in `execute`, once dry in the check. Both became `_walk(commands, obstacles)`, which answers where the commands take the rover and which obstacle stopped it, and `execute` now calls it twice: against what the rover has discovered, to decide whether to refuse, then against the world, to move. `_move` and `_turn` are gone — both were the mutating halves of that walk and nothing needs them any more. Suite green after each step.
**Commit:** dad45bd
**Also satisfied:** none
**Wrote:** `test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit` — same setup as the refusal test, `execute("FF")`, expects `rover.blocked_by == (3, 3)`. Fails with `assert None == (3, 3)`: the refusal returns before anything is reported, so the rover refuses silently.
**Interface decided:** none. `blocked_by` carries the refusal as well as the bump, which is what turn 14 named it for.
**List:** checked off "A refused command string reports which known obstacle the rover would have hit". Added nothing. Three items left, one of them the beyond-the-task one.
**Surprise:** "the rover can tell in advance" turned out to be the same walk as going there, not a second implementation of the rules. Twist 2 reads like it needs a planner; what it needed was for the walk to stop reading `self` and start taking a position, at which point predicting and doing are one function with different obstacles passed in. The refusal check is `self.discovered_obstacles`, the run is `self.obstacles`, and the difference between what the rover believes and what is true is now a single argument.

## Turn 22 — pong

**Received:** `test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit` failing with `assert None == (3, 3)` — the refusal returned before anything was reported.
**Green by:** Obvious Implementation — set `blocked_by` on the way out of the refusal.
**Refactored:** `blocked_by` was being written in three places by then: cleared at the top of `execute`, set on refusal, set on a bump. All three are the same sentence, so they became one line at the end and the eager clear went away — the walk already answers `None` when nothing stops it. `execute` now reads as: work out what the rover foresees; if it foresees nothing, go, and learn whatever it actually meets; either way, report what stopped it. Suite green after the change.
**Commit:** 78e82c3
**Also satisfied:** none
**Wrote:** no failing test. See the question below.
**Interface decided:** none.
**List:** checked off "Turning is fine either way: a command string of turns alone is never refused" (see below). One item left, and it is the one I added in turn 16 and marked as beyond the task.
**Regression test in the tree:** `test_a_command_string_of_turns_alone_is_never_refused` — the rover bumps (3, 3) to learn it, then runs `execute("LLRR")` and comes back to (3, 2, "N") unrefused. It passed as written. It is not a repeat of turn 16's turning test: that one proved turns cannot bump an *unknown* obstacle, this one proves they cannot trip the refusal on a *known* one, and it leaves the rover facing the obstacle it knows about, which is as close to refusal as a string of turns can get.
**Surprise:** every remaining item the task actually states was already true. The last three list items in a row went green on sight — order, turns-and-refusal, and before them the pole-backward item — and each was paid for by a refactoring made for an unrelated reason. Turn 21's `_walk` is the extreme case: it was extracted to remove duplication and it happens to make "turns are never refused" impossible to violate, because the refusal check and the turn handling are the same loop and turns never consult the obstacle argument. The list found nothing wrong at the end of this run. It did make someone go and look eight separate times, and twice what it found was a defect nobody would have written a test for otherwise.
**Question:** The only item left is one I added, not one the task gave us. `blocked_by` does not exist as an attribute until the first `execute` — a freshly built rover raises `AttributeError` when asked what stopped it. The task's report sentence begins "After any command string", so it is silent on the question, and turn 15 deliberately declined to answer it in the constructor for that reason. Three ways to go, and it is yours to pick: (a) it is in scope by implication, so a test says a new rover reports `None` and the constructor initialises it; (b) it is out of scope, so I strike the item and the list is finished as the task defined it, leaving the attribute as it is; (c) it is out of scope as behavior but the raggedness is not worth shipping, so initialise it as a refactoring with no test of its own and note it. I lean (a): the rover already has one attribute answering "what do you know" that exists from birth precisely because the task said "at any time", and having its neighbour raise instead is a difference the task never asked for. But it is your call, and the run is otherwise done — 26 tests, all green except that nothing is red right now.
**Suite:** `.venv/bin/pytest` from the repository root — 26 passed, 0 failed. No red test is standing; the baton goes to you rather than to ping.

## Turn 23 — pong

**Received:** the human's answer, not a test. The baton came back to `pong` with option (a) appended to `.real-tdd/task.md`: a rover that has not run a command string reports no obstacle, and every report the rover makes is readable at any time, including before the first command. No red test was standing, so there was no green step this turn — I resumed at Red.
**Green by:** n/a
**Refactored:** nothing
**Commit:** none. Nothing was green to commit; the last commit is still 78e82c3.
**Also satisfied:** none
**Wrote:** `test_a_rover_that_has_not_run_a_command_string_reports_no_obstacle` — a rover built with an obstacle at (3, 3) it has never met, asserting `rover.blocked_by is None` before any command string is run. Fails with `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Interface decided:** none new, but the answer settles something wider than the one attribute. The human's second sentence — every report readable at any time — makes "readable from birth" a property of the rover's reports as a class rather than a fact about `blocked_by`. `discovered_obstacles` already had it; now both do, and any report added later inherits the rule.
**List:** checked off "A rover that has not run a command string yet reports no obstacle", annotated with where it came from and who ruled it in scope. The list is now empty. Two tests remain uncommitted in the tree: this red one, and `test_a_command_string_of_turns_alone_is_never_refused` from turn 22, which is a regression test and belongs in whatever commit makes this red one green.
**Surprise:** the item that ended the run is the only one that was not in the task when the run started. It came from a green in turn 15 that deliberately left a question unanswered, survived seven turns on the list marked "not asked for by the task", and was settled by the human rather than by either session. That is the whole apparatus working as designed: the list held a behavior that had no test, the journal carried the reason it had no test across four handovers, and the one decision neither session was entitled to make went to the person who was entitled to make it.
**Suite:** `.venv/bin/pytest` from the repository root — 26 passed, 1 failed.

## Turn 24 — ping

**Received:** `test_a_rover_that_has_not_run_a_command_string_reports_no_obstacle` failing with `AttributeError: 'Rover' object has no attribute 'blocked_by'`. Also received `test_a_command_string_of_turns_alone_is_never_refused` as an uncommitted regression test; it went into this turn's commit.
**Green by:** Obvious Implementation — `self.blocked_by = None` in the constructor, next to `discovered_obstacles`. Turn 15 declined to write this exact line because no test demanded it and the task was silent; the human ruled it in, so it is now one line with a test under it.
**Refactored:** nothing. The two reports sit next to each other in the constructor and read as a pair, which is what the human's answer said they are.
**Commit:** 69a4aeb
**Also satisfied:** none
**Wrote:** no failing test. The list is empty.
**Interface decided:** none.
**List:** empty. Every item the task stated has a test, plus the one item this run added and the human ruled in scope.
**Surprise:** none this turn. The closing observation belongs to the run rather than to the turn, so it is below.

## End of run — ping

Twenty-four turns, thirteen commits after the scaffold, 27 tests, all
green. `mars_rover/__init__.py` is one class, six methods, sixty lines.
The baton reads `done`; the human decides whether the list was finished.

What the two-session split actually produced, as distinct from what one
session writing tests for itself would have:

- **Three defects were found by the list, not by a test.** The pole turn
  surviving a blocked crossing (flagged turn 13, tested turn 16, fixed
  turn 17), the stale `blocked_by` after a clean run, and the missing
  step-table rows a rover facing south or west would have crashed on.
  Each was written into the journal by the session that saw it and left
  for the other, because fixing it silently would have been production
  code no test demanded.
- **Five items turned out to be already true when their turn came.**
  Backward across a pole, discovery order, turns never bumping, turns
  never being refused, and the west wrap. Every one had been paid for by
  a refactoring done for an unrelated reason. None was a bug. All five
  were unverified until the list made someone go and look, which is the
  clearest thing the list did all run.
- **One test can only ever have been red once.** Turn 19's
  no-duplicate-discoveries test was written deliberately ahead of the
  refusal rule, because once a rover refuses strings that would hit what
  it knows, it can never bump a known obstacle again and the rule becomes
  unobservable from outside. It passes today for a reason unrelated to
  its name.
- **The one decision neither session was entitled to make went to the
  human.** Whether a rover that has never run a command string reports
  `None` or raises. It sat on the list for seven turns marked "not asked
  for by the task" and was answered in `task.md`, not by either session.

The rhythm the two contexts produced, which one context would have to
simulate: a test arrived as an instruction with no explanation attached,
and the session receiving it had to work out what behavior it was asking
for from the failure alone. Twice that produced a green the writer had
not imagined — turn 6's heading cycle, which the pole crossing later
reused whole, and turn 21's `_walk`, extracted to remove duplication,
which turned out to be the entire answer to "the rover can tell in
advance". Neither was planned; the skill forbids planning; both came out
of a refactoring step under a test written by someone who could not see
the implementation.

The journal is the data. It is `.real-tdd/journal.md`, and the honest
entries are the ones that say "none".
