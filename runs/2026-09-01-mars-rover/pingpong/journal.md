# Journal — Mars Rover real-tdd run

## Turn 1 — ping — 2026-09-01T19:23:38Z

**Received:** nothing; first turn.
**Green by:** n/a
**Refactored:** nothing
**Commit:** 1838ae5 (scaffold: pyproject with pytest via uv, empty `tests` package, test list; no production code)
**Wrote:** `test_new_rover_reports_its_starting_position_and_heading` — fails because `ModuleNotFoundError: No module named 'mars_rover'` at collection.
**List:** checked "A new rover reports the position and heading it was created with". Wrote the whole list fresh (41 items) across creation, turning, moving, wrap, poles, unknown obstacles, learning, odds and ends.
**Surprise:** writing the list forced me to notice that "B across a pole" is under-specified by the task in a way that "F across a pole" is not: the task says backward crosses "the same way a forward move in the opposite heading would", which means a rover heading S on the north pole row that reverses ends up heading N, not S. I wrote that expectation into the list item rather than leaving it vague. Also noticed the task never says what "reports" looks like for the refused-vs-bumped distinction; the list keeps them as separate items so the test that pins each one down is a separate design decision.

Suite: `uv run pytest` (uv creates the venv and installs pytest on first run).

## Turn 2 — pong — 2026-09-01T19:31:05Z

**Received:** `test_new_rover_reports_its_starting_position_and_heading` failing because `ModuleNotFoundError: No module named 'mars_rover'` at collection — no production code existed at all.
**Green by:** Obvious Implementation — storing the five constructor arguments and exposing two of them is not something I could get wrong, and Fake It here would have meant hard-coding `(2, 3)`, which the test could not distinguish but which would have taught nobody anything.
**Refactored:** nothing. Two assignments, no duplication to remove. `width` and `height` are accepted and dropped on the floor because the test names them but demands nothing of them; I did not store them, since no test asks.
**Commit:** d5c8cf9
**Wrote:** `test_turning_left_from_north_heads_west` — fails because `AttributeError: 'Rover' object has no attribute 'execute'`.
**List:** checked "`L` from N heads W". Split the original item, which bundled all four left-turn cases, into the one case I tested and a new item holding the remaining three (W→S, S→E, E→N). Added nothing else.
**Surprise:** the constructor test already forced two interface decisions I did not get a vote on — that position is one tuple rather than two attributes, and that headings are strings rather than an enum — and both are now load-bearing for everything after. It is a sharper illustration of the Starter Test than I expected: the "trivial" test that only establishes where the code lives had already fixed the vocabulary of the whole rest of the run before any behavior existed. I also had to decide, writing the Red, whether `L` from N heads W belongs in one test with the other three turns; I kept it to one case so the step stays small and left the choice of whether to generalize now or triangulate to whoever takes it.

## Turn 3 — ping — 2026-09-01T19:25:59Z

**Received:** `test_turning_left_from_north_heads_west` failing because `AttributeError: 'Rover' object has no attribute 'execute'`.
**Green by:** Fake It — one turn example cannot justify a turn table, and my partner's journal said they had deliberately left the generalize-now-or-triangulate choice open. `execute` assigns the constant `"W"` and ignores its argument. That constant is the duplication the next test is meant to break.
**Refactored:** nothing. With a single example there is no abstraction to extract; the duplication between the constant and the test's expected value is real but not yet removable.
**Commit:** 58e0b30
**Wrote:** `test_turning_left_from_west_heads_south` — fails because `assert 'W' == 'S'`: the faked constant answers every left turn with W.
**List:** checked "`L` from W heads S". Split the remaining left-turn item again, leaving "from S heads E, from E heads N" open, so the next taker can decide whether two examples are enough to generalize or a third is wanted.
**Surprise:** the human's mid-turn housekeeping note revealed that neither of us had committed `tests/test_rover.py` at all. My partner's green commit contained only `mars_rover.py`, and my own scaffold commit predated the test, so two "clean check-ins" had both left the tests untracked without either session noticing. The suite was green in the working tree and would have been empty on a fresh clone. Nothing in Beck's rhythm catches that, because the rhythm assumes the pair share a screen and a repository state that someone is looking at; here the only thing either session inspects is the test run, and the test run does not care what is committed. I amended 58e0b30 to track the tests and the run's bookkeeping files.

## Turn 4 — pong — 2026-09-01T19:38:20Z

**Received:** `test_turning_left_from_west_heads_south` failing because `assert 'W' == 'S'` — `execute` returned the faked constant `"W"` for any heading.
**Green by:** Triangulate — two examples, N→W and W→S, are exactly the case Beck reserves triangulation for, and the smallest thing that answers both without listing them is the compass cycle. I introduced a `COMPASS` tuple in clockwise order and stepped back one place.
**Refactored:** the constant `"W"` was the duplication between test and code, and generalizing removed it; there was nothing left over afterwards.
**Commit:** 45e1cde (this one carries `tests/test_rover.py` as well, per the human's housekeeping note; the two passing tests are now tracked and only the new red is loose)
**Wrote:** `test_turning_right_from_north_heads_east` — fails because `assert 'W' == 'E'`: `execute` still turns left whatever letter it is handed.
**List:** checked "`L` from W heads S" and "`R` from N heads E". Split the right-turn item the way the left-turn one was split, leaving E→S, S→W, W→N open. Annotated the remaining left-turn item to record that the compass cycle already answers it, so whoever picks it finds a test that passes on arrival rather than a step.
**Surprise:** the generalization overshot the tests on purpose and I could not avoid it. Stepping back around a four-element cycle answers S→E and E→N as well, so two of my partner's list items were satisfied by code no test had asked for. Beck's rule against writing undemanded code and his triangulation pattern point in opposite directions here: any abstraction over a cyclic domain covers the whole cycle or it is still a lookup table. The list, not the suite, is what caught it — I had to go annotate items that had silently become untestable-as-steps. That is the first time in this run that the list did work the tests could not.

## Turn 5 — ping — 2026-09-01T19:28:02Z

**Received:** `test_turning_right_from_north_heads_east` failing because `assert 'W' == 'E'` — the compass step was hard-coded to -1, so every command turned left.
**Green by:** Obvious Implementation — with the cycle already in place, left and right are the same step with opposite signs. A `TURNS` lookup maps the letter to the sign; nothing about that could surprise me, so Fake It would have been ceremony.
**Refactored:** pulled the stepping expression out of `execute` into `_turned`, so the method reads as "turn by this much" rather than as modular arithmetic. No duplication was removed; there was one call site. I did it because the arithmetic will need a second reader when backward moves arrive.
**Commit:** 0688493
**Wrote:** `test_moving_forward_heading_north_increases_latitude` — fails with `KeyError: 'F'` from the `TURNS` lookup.
**List:** checked "`F` heading N increases y by one". Added nothing.
**Surprise:** `execute` still indexes `TURNS` with the entire argument, not with a character, and no test has objected because every command string so far has been one letter long. The interface says "a string of commands" and the code has quietly been treating it as "a command". My partner's note about the compass cycle overshooting its tests has an exact mirror here: that generalization did more than the tests demanded, and this one does less, and in both cases the suite is silent. The `KeyError` I just got is the code complaining about an unknown command, which is the right red for the wrong reason, and it will be a `KeyError` again the first time someone writes `FF`.

## Turn 6 — pong — 2026-09-01T19:45:12Z

**Received:** `test_moving_forward_heading_north_increases_latitude` failing with `KeyError: 'F'` — `execute` looked every command up in the turn table.
**Green by:** Fake It — I know what the heading-to-delta table looks like, but writing it would have answered three more list items with code no test asked for, exactly the overshoot the compass cycle caused two turns ago. Movement over four headings is a lookup table rather than a cycle, so a partial one is coherent in a way half a cycle is not. `execute` now branches on whether the command is a turn, and any non-turn adds one to latitude.
**Refactored:** nothing. The branch is the first structure in `execute` and there is no second copy of it to fold together yet.
**Commit:** 1c447dd
**Wrote:** `test_moving_forward_heading_east_increases_longitude` — fails because the position comes back `(2, 4)` instead of `(3, 3)`: the faked move goes north whatever the heading.
**List:** checked "`F` heading E increases x by one". Added nothing.
**Surprise:** taking Fake It deliberately, against my own confidence, felt like the first genuinely different move this technique has produced. My partner's `KeyError` observation was right and I inherited its mirror image: `execute` still treats the whole argument as one command, and the branch I added made that worse, because now any unrecognized string quietly moves the rover north instead of raising. `FF` no longer fails loudly; it fails silently by moving one square. The suite is still fully green and says nothing about it. Neither of us has written a test that would notice, and the list item that would — the one about `FFRFF` — is still open.

## Turn 7 — ping — 2026-09-01T19:29:36Z

**Received:** `test_moving_forward_heading_east_increases_longitude` failing with `assert (2, 4) == (3, 3)` — the faked move went north whatever the heading.
**Green by:** Triangulate — two headings were exactly what the abstraction needed, and the abstraction here is a lookup rather than a cycle, so I could take my partner's point and build a `STEPS` table holding only N and E. The two untested headings raise `KeyError` instead of moving north, which is the overshoot problem solved by leaving the table incomplete on purpose.
**Refactored:** extracted `_moved` alongside `_turned`, so `execute` reads as a choice between turning by a step and moving by a step, and the tuple arithmetic sits in one place.
**Commit:** 77240ce
**Wrote:** `test_a_command_string_runs_its_commands_in_order` — fails with `assert (0, 1) == (2, 2)`: `execute` consumed `"FFRFF"` as a single unrecognized command and moved one square north.
**List:** checked "A command string executes in order". Added nothing.
**Surprise:** the hole both of us had written about turned out to be free to close. I expected the multi-command test to be too big a step, because it looked like it needed the full delta table, and it does not: `FFRFF` from the origin uses only north and east, both of which the table already holds. The step both of us had been flagging as dangerous was available all along and neither journal entry noticed, because we were each describing the defect rather than sizing the test that would expose it. Also worth recording that the red I got is a wrong answer, not a `KeyError`, which is the failure mode my turn-5 entry predicted would go silent.

## Turn 8 — pong — 2026-09-01T19:52:40Z

**Received:** `test_a_command_string_runs_its_commands_in_order` failing with `assert (0, 1) == (2, 2)` — `"FFRFF"` fell through the turn branch and moved one square north, the silent failure my last entry described.
**Green by:** Obvious Implementation — a loop over the characters is not something I could get wrong, and the per-command body already existed intact; it only had to stop being the whole method.
**Refactored:** split `execute` into the loop and `_execute_one`, which is now the thing the turn and move branches live in. That is the same extraction my partner did for `_turned` and `_moved`, one level up: `execute` is a sentence about the string, `_execute_one` a sentence about a letter.
**Commit:** 805adcd
**Wrote:** `test_moving_backward_goes_opposite_the_heading_without_turning` — fails because the position comes back `(2, 4)` instead of `(2, 2)`: `B` is not a turn, so it takes the forward branch.
**List:** checked "`B` moves one square opposite to the heading, heading unchanged". Added nothing.
**Surprise:** the else-branch is now doing two jobs and only one test has ever noticed. Anything that is not `L` or `R` moves forward, so `B` moves north, and so would `Q`. I could have closed that by making the branch explicit while I was in there, and did not, because no test demanded it and the red I wrote is precisely the test that does. Writing the red immediately after deciding not to fix the thing it targets is a strange feeling: I knew the defect, knew the fix, and the rule that I may only hand over a test meant the fix had to travel as a failing assertion instead of as code. That is the mechanism working, and it is the first time this run that it cost me something to obey it.

## Turn 9 — ping — 2026-09-01T19:30:59Z

**Received:** `test_moving_backward_goes_opposite_the_heading_without_turning` failing with `assert (2, 4) == (2, 2)` — `B` fell through to the forward branch.
**Green by:** Obvious Implementation — backward is forward with the delta negated, and I have no doubt about that. A `SENSES` table gives the sign, and as a side effect the else-branch stopped accepting any letter at all: an unknown command now raises rather than moving north. My partner's entry flagged that hole and the test they wrote is what let it close.
**Refactored:** nothing beyond threading the sense through `_moved`. The method still has one job.
**Commit:** c5922e8
**Wrote:** `test_moving_east_off_the_last_column_wraps_to_the_first` — fails with `assert (10, 3) == (0, 3)`: the rover walks off the edge of the map.
**List:** checked "`F` heading E from the last column lands on column 0". Added nothing.
**Surprise:** `width` and `height` have been accepted and thrown away since turn 2, and this is the first test in nine turns that needs one of them back. My partner noted at the time that they were dropping them because no test asked; the constructor has been carrying two arguments that were pure documentation ever since, and every test has passed `width=10, height=10` out of politeness to a signature that ignored them. It is a cleaner demonstration than I expected of the rule about not writing undemanded code: the arguments were in the interface from the first test, and the behavior behind them took nine turns to arrive.

## Turn 10 — pong — 2026-09-01T20:00:15Z

**Received:** `test_moving_east_off_the_last_column_wraps_to_the_first` failing with `assert (10, 3) == (0, 3)` — the rover walked off the last column.
**Green by:** Obvious Implementation — a modulo on the longitude is the whole of it. `width` is stored for the first time since the constructor was written; `height` is still discarded because nothing asks for it yet.
**Refactored:** nothing. The modulo went where the arithmetic already lived.
**Commit:** d22c309
**Wrote:** `test_moving_north_off_the_north_pole_row_crosses_the_pole` — fails with `assert (2, 5) == (7, 4)`: latitude ran off the top of the map instead of crossing the pole.
**List:** checked the north-pole item. Annotated two wrap items, west-off-column-zero and backward wrapping, because Python's modulo takes negative operands and both now pass on arrival; that is the third time a generalization has swallowed list items ahead of their tests.
**Surprise:** I chose a five-row planet for the pole test and only afterwards noticed that every test before it had said `height=10` for no reason at all. The pole test is the first one where the number matters, and picking it forced me to think about which row is the pole row, which is a fact the constructor has been carrying silently for ten turns. There is a pattern here that neither of us planned: each twist in the task has arrived as an argument that existed long before its behavior did. The interface was fixed by the Starter Test and the behaviors have been filling it in ever since, which is the opposite of the story where tests drive the interface.

## Turn 11 — ping — 2026-09-01T19:32:32Z

**Received:** `test_moving_north_off_the_north_pole_row_crosses_the_pole` failing with `assert (2, 5) == (7, 4)` — latitude ran off the top of the map.
**Green by:** Obvious Implementation — the three things the pole does are all stated outright in the task, and the about-face turned out to be a compass step of two, so `_turned` did that half for free. `height` is stored, one turn after `width` was.
**Refactored:** `_moved` became `_move` and now sets position and heading together, because crossing a pole changes both and returning a pair for the caller to unpack put the same knowledge in two places. Also extracted `_antipode`, since "the longitude on the far side" deserves its own name. Only the north crossing exists; nothing is generalized over both poles yet.
**Commit:** 606f08d
**Wrote:** `test_moving_forward_heading_south_decreases_latitude` — fails with `KeyError: 'S'` from the step table.
**List:** checked "`F` heading S decreases y by one". Added nothing.
**Surprise:** I went to write the south pole crossing and could not, because the step table still has no entry for heading S and the test would have failed on the missing delta rather than on the missing pole. The twist and the plain case are tangled: you cannot test the south pole without first being able to walk south at all. That is Beck's Child Test arriving unprompted, and the thing that produced it was not judgment about step size but the concrete failure the code would have given me. I only found it by asking what the red would say, which is a question the Red rules make you answer and that a plan would not have.

## Turn 12 — pong — 2026-09-01T20:07:30Z

**Received:** `test_moving_forward_heading_south_decreases_latitude` failing with `KeyError: 'S'` — the step table still held only north and east.
**Green by:** Obvious Implementation — one entry in a table whose shape three tests have already fixed. I added south alone and left west out, keeping the table deliberately short the way it has been since turn 7.
**Refactored:** nothing. A dictionary entry has no duplication to remove.
**Commit:** 90a771a
**Wrote:** `test_moving_south_off_the_south_pole_row_crosses_the_pole` — fails with `assert (2, -1) == (7, 0)`: latitude runs off the bottom, since only the north crossing exists.
**List:** checked the south-pole item. Added nothing.
**Surprise:** none. My partner's last entry had already found the interesting thing, that the south pole test was blocked behind the missing south step, and this turn was the two halves of that observation landing in order. Worth recording that the whole turn was three lines of change and that the blocking test my partner wrote made it feel inevitable rather than chosen, which is what a well-sized step is supposed to feel like.

## Turn 13 — ping — 2026-09-01T19:33:43Z

**Received:** `test_moving_south_off_the_south_pole_row_crosses_the_pole` failing with `assert (2, -1) == (7, 0)` — only the north crossing existed.
**Green by:** Triangulate — with a crossing at each end I could see the shared rule, which is that the crossing fires when latitude leaves the map and the rover is put back on the row it came from. Clamping does that for both poles in one line.
**Refactored:** the generalization was the refactor. The north-specific condition and its north-specific clamp were the duplication, and both are gone.
**Commit:** 6a6c291
**Wrote:** `test_moving_forward_heading_west_decreases_longitude` — fails with `KeyError: 'W'` from the step table.
**List:** checked "`F` heading W decreases x by one". Added nothing.
**Surprise:** the pole generalization is the first one in this run that did not overshoot, and the reason is that the two examples sat at opposite ends of the same axis rather than being two of four cases in a table. The compass cycle swallowed two list items and the step table has been filled in one entry per turn precisely because a table has no shape to generalize over. Four turns in a row have now been "add one entry", which is boring in exactly the way Beck's stopping rule describes, and the interesting steps have all been the ones where two examples bracketed something.

## Turn 14 — pong — 2026-09-01T20:14:55Z

**Received:** `test_moving_forward_heading_west_decreases_longitude` failing with `KeyError: 'W'` — the last missing entry in the step table.
**Green by:** Obvious Implementation — the fourth of four entries, with three already fixing the shape.
**Refactored:** nothing, and I want to record the thing I decided not to do. The step table and the compass tuple now both encode the order of the four headings, which is duplication of a kind, and it could be removed by deriving each step from the heading's index. I left it. The derivation would be arithmetic standing in for a fact that is currently readable at a glance, and Beck's target is duplicated knowledge that has to be changed in two places, which this is not: nobody will ever add a fifth compass point.
**Commit:** 48722d6
**Wrote:** `test_moving_into_an_unknown_obstacle_leaves_the_rover_in_place` — fails with `TypeError: Rover.__init__() got an unexpected keyword argument 'obstacles'`.
**List:** checked "`F` heading W decreases x by one". Split the first unknown-obstacle item, which bundled staying put with reporting the obstacle, into those two halves and checked only the first.
**Surprise:** writing that red meant deciding, alone and in one line, how the world tells the rover where the rocks are, and the twist makes the decision sharper than the classic problem does. The rover must not know the map, but something has to know it, and I chose to hand the obstacles to the constructor and keep the rover's own discoveries as a separate thing it will have to accumulate. A planet object holding the terrain was the other candidate and I passed on it, not because it is worse but because it would have rewritten every existing test's first line, and a red that forces a fourteen-test rename is not a step. That is a real design decision made under pressure from step size rather than from taste, and the interface will carry it for the rest of the run.

## Turn 15 — ping — 2026-09-01T19:35:37Z

**Received:** `test_moving_into_an_unknown_obstacle_leaves_the_rover_in_place` failing with `TypeError: unexpected keyword argument 'obstacles'`.
**Green by:** Obvious Implementation — an optional constructor argument and a membership check. I took my partner's design as given rather than reopening it; the test is the specification and it says the obstacles arrive through the constructor.
**Refactored:** split `_move` into working out where the move would land and taking it. The obstacle check needs the destination before the rover commits to it, and the pole crossing was computing that destination inside the act of moving. `_destination` is now pure and returns the square and the heading the rover would have, which also means a refused move keeps its heading for free.
**Commit:** 0c69608
**Wrote:** `test_the_rover_reports_the_obstacle_it_stopped_at` — fails with `AttributeError: 'Rover' object has no attribute 'stopped_by'`.
**List:** checked "reports it was stopped by that obstacle". Added nothing.
**Surprise:** the refactor the obstacle forced is one I would not have made otherwise, and it is the first time in this run that a twist improved the classic code rather than sitting beside it. Separating "where would this land" from "go there" is what makes the pole crossing testable as a value, and it arrived because an obstacle needs to veto a move that has already been fully computed. My partner's constructor decision, which they described as chosen under step-size pressure rather than taste, turned out to pay a dividend they did not predict: because the rocks are known to the object, the veto is a pure question about a square, and the look-ahead that twist two demands will be able to ask that same question without moving.

## Turn 16 — pong — 2026-09-01T20:22:40Z

**Received:** `test_the_rover_reports_the_obstacle_it_stopped_at` failing with `AttributeError: 'Rover' object has no attribute 'stopped_by'`.
**Green by:** Obvious Implementation — one assignment on the path that already knew the answer. `_destination` had made the blocked square a value my partner's refactor handed me, so the report was a matter of keeping it rather than recomputing it.
**Refactored:** nothing, and again the interesting part is what I left alone. `stopped_by` exists only after a bump; a rover that has never hit anything has no such attribute at all. Initialising it to `None` in the constructor is one line and I did not write it, because the list item that demands it is still open and would then pass on arrival. The code is uglier than I would leave it in ordinary work and the rule is the reason.
**Commit:** 3cefdce
**Wrote:** `test_a_bump_abandons_the_rest_of_the_command_string` — fails with `assert 'E' == 'N'`: after the blocked `F` the loop went on and executed the `R`.
**List:** checked "After bumping, the rest of the command string is abandoned". Added nothing.
**Surprise:** the test I wrote asserts on the heading and never mentions position, which is not how I would have described "the rest of the string is abandoned" in prose. A turn is the cheapest observable proof that the loop kept going, because the blocked move leaves no trace by design. Assert First did that: starting from what could be observed rather than from what the behavior is called produced a test about turning to demonstrate a rule about moving.

## Turn 17 — ping — 2026-09-01T19:37:02Z

**Received:** `test_a_bump_abandons_the_rest_of_the_command_string` failing with `assert 'E' == 'N'` — the loop ran the `R` after the blocked `F`.
**Green by:** Obvious Implementation — the loop needs to hear about the bump, so executing one command now answers whether it was blocked and the loop breaks on the first true. Turns answer false, which is the task's "turning never hits anything" stated in the one place it has to be.
**Refactored:** nothing. The boolean threading through two small methods is the whole change and there is no second copy of it.
**Commit:** 8410f78
**Wrote:** `test_a_rover_that_has_hit_nothing_reports_no_obstacle` — fails with `AttributeError: 'Rover' object has no attribute 'stopped_by'`, the attribute my partner deliberately left uninitialised last turn.
**List:** checked "After a command string with no obstacle, the rover reports that it did not stop for an obstacle". Added nothing.
**Surprise:** my partner wrote in their journal that they had left `stopped_by` missing on purpose and that the code was uglier than they would leave it, and the effect on me was to make the next test obvious rather than to make me want to fix it. The journal is doing something the working tree cannot: the tree shows a missing attribute, which reads as an oversight, and the entry shows a deliberate hole, which reads as a handoff. That is the closest thing to conversation this arrangement has produced, and it worked without either of us telling the other what to do, which the rules forbid.

## Turn 18 — pong — 2026-09-01T20:30:05Z

**Received:** `test_a_rover_that_has_hit_nothing_reports_no_obstacle` failing with `AttributeError: 'Rover' object has no attribute 'stopped_by'` — the hole I left open two turns ago, now with a test demanding it be filled.
**Green by:** Obvious Implementation — the one line in the constructor I had declined to write until something asked for it.
**Refactored:** nothing.
**Commit:** 2fe4701
**Wrote:** `test_a_new_rover_has_discovered_no_obstacles` — fails with `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`.
**List:** checked "A new rover has discovered no obstacles". Added nothing.
**Surprise:** the red I wrote hands a rock to the constructor and then asserts the rover knows nothing about it, which is twist two stated in three lines with no machinery behind it yet. Writing it made me notice that the rover's own knowledge and the planet's terrain now have to be two separate things inside one object, and that the constructor argument my step-size worry picked back in turn 14 is what makes that awkward rather than natural. A planet object would have put the split where it belongs. The test can still say the right thing about behavior, which is the part that matters, but the interface is carrying a decision that the tests did not drive and cannot now undo cheaply.

## Turn 19 — ping — 2026-09-01T19:38:22Z

**Received:** `test_a_new_rover_has_discovered_no_obstacles` failing with `AttributeError: 'Rover' object has no attribute 'discovered_obstacles'`.
**Green by:** Obvious Implementation — an empty tuple in the constructor.
**Refactored:** renamed the stored rocks from `obstacles` to `terrain`. My partner's entry said the two kinds of knowledge now have to live in one object and that the name makes that awkward; the constructor argument is theirs and the tests depend on it, so I left the argument alone and changed only what the object calls the thing it stores. `terrain` is what the planet has and `discovered_obstacles` is what the rover knows, and now the two lines of the constructor say so.
**Commit:** 193c46f
**Wrote:** `test_bumping_an_obstacle_discovers_it` — fails with `assert () == ((2, 4),)`.
**List:** checked "After bumping, the rover lists that obstacle as discovered". Added nothing.
**Surprise:** the rename cost nothing and no test noticed, which is the first evidence in this run that the suite is holding the interface rather than the implementation. Every earlier refactor was invisible because it was inside a method; this one moved a piece of state and renamed it, and eighteen tests stayed silent because none of them had ever reached past `position`, `heading`, `stopped_by` and `execute`. My partner's worry that the interface is carrying an undriven decision is right about the constructor argument, and wrong about the inside of the object, where the decision turned out to be free to reverse.

## Turn 20 — pong — 2026-09-01T20:37:50Z

**Received:** `test_bumping_an_obstacle_discovers_it` failing with `assert () == ((2, 4),)`.
**Green by:** Obvious Implementation — one append on the branch that already recognised the bump. I did not deduplicate, because the item that asks for that is still open and I would rather hand it over as a failing test than as code.
**Refactored:** nothing. The blocked branch now does three things in a row, which is a list rather than a tangle.
**Commit:** 40e7bcf
**Wrote:** `test_bumping_the_same_obstacle_twice_lists_it_once` — fails because the discovered list comes back holding the same rock twice.
**List:** checked "Bumping the same obstacle twice lists it once". Annotated the discovery-order item, since appending to a tuple answers it already; that is the fourth item in this run swallowed by a generalization before its test existed.
**Surprise:** my new test bumps the same rock twice in two command strings, and by the second one the rock is no longer unknown, so the same three lines will have to keep meaning what they say once refusal exists and the second `F` stops being a bump at all. I wrote it without noticing that at first, and only saw it when I asked why two `execute` calls rather than one string. A test that survives a behavior change it never mentioned is worth more than the item that prompted it, and asserting on what the rover knows rather than on how it stopped is what bought that.

## Turn 21 — ping — 2026-09-01T19:40:08Z

**Received:** `test_bumping_the_same_obstacle_twice_lists_it_once` failing with `assert ((2, 4), (2, 4)) == ((2, 4),)`.
**Green by:** Obvious Implementation — an existence check before the append.
**Refactored:** pulled the append into `_discover`, so the blocked branch reads as reporting the stop and recording what was learned rather than as tuple arithmetic. That is the same move my partner declined last turn for the right reason: they would have been writing the deduplication before its test.
**Commit:** 7841b0f
**Wrote:** `test_a_command_string_that_would_hit_a_known_obstacle_is_refused_whole` — fails with `assert (2, 4) == (2, 3)`: the rover took the first `F` and stopped at the rock instead of refusing the string.
**List:** checked the refusal item, and split off the heading half of it, which the test I wrote does not cover.
**Surprise:** it took real work to build a situation where refusal and bumping look different from the outside. For a single `F` into a known rock they are identical: the rover ends up in the same square either way, and only the report could tell them apart. The difference is observable only when the rock is more than one command deep, and the rover cannot know a rock without having bumped it, so the test has to bump, retreat, and then approach again from two squares out. Three `execute` calls to set up one assertion is more ceremony than any test in this run, and the twist's whole point lives in the gap between the second and third.

## Turn 22 — pong — 2026-09-01T20:47:20Z

**Received:** `test_a_command_string_that_would_hit_a_known_obstacle_is_refused_whole` failing with `assert (2, 4) == (2, 3)` — the rover walked the first `F` and stopped at the rock rather than refusing the string.
**Green by:** Obvious Implementation — refusal is a dry run of the string before the real one, and the shape of it was clear. The dry run only consults what the rover has discovered, not the terrain, so an unknown rock does not stop the look-ahead; the item that asks for that is still open and I left it to a test.
**Refactored:** twice, and the first version was a sin I wrote knowing I would remove it. Getting to green, the look-ahead mutated the rover's own position and heading and restored them afterwards, because `_destination` and `_turned` both read state off `self`. Then I made both take the position and heading they should work from, so the dry run walks local variables and the real move walks the rover. The duplication removed was between simulating and moving: those were the same arithmetic reachable only by pretending to move.
**Commit:** 393fa23
**Wrote:** `test_a_later_command_string_does_not_still_report_an_earlier_bump` — fails with `assert (2, 4) is None`.
**List:** checked the report-clearing item. Annotated the refusal-report item with why it cannot be tested yet.
**Surprise:** the test I meant to write passed on arrival and the rules made me throw it away, which turned out to be the most informative moment of the run. I wrote the refused string's report, and it was green immediately, because `stopped_by` still held the rock from the bump that taught the rover about it. Refusing and merely remembering are indistinguishable from outside while a stale report is never cleared. So the item I wanted was blocked behind an odds-and-ends item nobody had thought was urgent, and the rule against keeping a passing test is what surfaced the dependency. My partner spent a whole turn building an elaborate three-string setup to make refusal observable; the thing that actually makes it observable is clearing the report, and neither of us saw that until a green bar appeared where a red one belonged.

## Turn 23 — ping — 2026-09-01T19:42:15Z

**Received:** `test_a_later_command_string_does_not_still_report_an_earlier_bump` failing with `assert (2, 4) is None`.
**Green by:** Obvious Implementation — clear the report at the top of `execute`. I put the clear before the refusal check rather than after, so a refused string reports nothing at all until something demands otherwise, which is what my next test does.
**Refactored:** nothing.
**Commit:** 1f827fc
**Wrote:** `test_a_refused_command_string_reports_the_known_obstacle_in_the_way` — fails with `assert None == (2, 5)`, which is the red my partner could not get last turn.
**List:** checked the refusal-report item.
**Surprise:** my partner's discarded test came back green-free one turn later without anyone doing anything to it. They wrote it, found it passing for the wrong reason, threw it away, and wrote the odds-and-ends test that the stale report was hiding behind; clearing the report is what turned their original assertion into a real one. The dependency ran the opposite way from how the list is organised. The refusal items sit in the twist-two section and read as the hard part, and the thing blocking them was a housekeeping item at the bottom of the file that neither of us would have prioritised. I also reused their exact scenario and only changed the assertion, so the setup ceremony I complained about two turns ago has now paid for two tests.

## Turn 24 — pong — 2026-09-01T20:55:40Z

**Received:** `test_a_refused_command_string_reports_the_known_obstacle_in_the_way` failing with `assert None == (2, 5)` — refusal was silent because my partner had put the report-clearing line above it.
**Green by:** Obvious Implementation — the look-ahead already knew which rock it had found and was throwing that away to return a boolean. It now returns the rock or nothing, and `execute` reports it. The predicate name went with the boolean, so `_would_hit_known_obstacle` became `_known_obstacle_ahead`.
**Refactored:** the rename was the refactor, and it is the second time in this run that turning a yes-or-no answer into the thing itself removed work rather than adding it. The same move is still available in `_execute_one`, which returns whether it was blocked while `stopped_by` holds what blocked it.
**Commit:** 7f70da6
**Wrote:** `test_an_unknown_obstacle_before_a_known_one_is_bumped_not_refused` — fails with `assert (2, 3) == (2, 4)`: the rover refused the whole string because the look-ahead walked straight through the rock it has never met.
**List:** checked "A command string that would hit an unknown obstacle before reaching a known one is not refused".
**Surprise:** this test needed a rover that has bumped one rock and then travelled to the far side of another, and there is no way to arrange that except to drive it there. The setup is a seven-command string whose only purpose is to walk around a rock the rover already knows about, and the string had to avoid that rock or the refusal I was setting up would have eaten the setup itself. Everything about the rover's knowledge is path-dependent, so the tests for twist two cannot use literal setup the way every earlier test did; they have to earn their state. Beck's Isolated Test rule holds, since each test drives its own rover from scratch, but the evident-data half of Assert First is gone and I do not think it can come back.

## Turn 25 — ping — 2026-09-01T19:46:34Z

**Received:** `test_an_unknown_obstacle_before_a_known_one_is_bumped_not_refused` failing with `assert (2, 3) == (2, 4)` — the look-ahead walked straight through a rock the rover has never met and refused the string on a known rock behind it.
**Green by:** Obvious Implementation — the look-ahead now stops at the first square that would really block the rover and refuses only if that square is one the rover has discovered. The rover consults the terrain it cannot see, which is a physical fact about what would happen rather than knowledge it acts on, and it is unobservable in any other scenario.
**Refactored:** nothing.
**Commit:** 75ee3d8
**Wrote:** nothing. No item on the list can be turned into a failing test.
**List:** twenty items left, and I checked every one of them off as a regression. I probed each behavior before writing anything, and all twenty already held. They are now twenty tests in a labelled block at the bottom of the file, committed as fa4e002, and the commit message and the comment above them both say they are not steps.
**Surprise:** the list stopped being able to fail somewhere around turn 20 and neither of us noticed for five turns, because we kept picking the items that could still fail and there were always a few. Four generalizations swallowed items ahead of their tests, my partner counted them as they went, and the count is what should have warned us: the compass cycle, the longitude modulo, the tuple append, and the pole clamp between them answered a third of the list before anyone asked. What is left at the end is a suite where twenty-four tests drove the code and twenty document it, and only the journal records which is which. Beck's stopping rule is about fear turning into boredom, and this run reached the boredom by a route he does not describe: not because the remaining behaviors are dull, but because the code got there first.

**Run over.** 44 tests, 24 of them steps. Baton set to `done`. The human decides whether the list was really finished.
