# Journal

## Turn 1 — ping — Tue Sep  1 21:06:51 UTC 2026

**Received:** nothing — this turn starts the run.
**Green by:** n/a — no test existed to make pass.
**Refactored:** nothing
**Commit:** bb4d514 — setup only, no production code: an empty root
`conftest.py` so pytest puts the repo root on `sys.path`, plus
`.real-tdd/test-list.md`.
**Also satisfied:** none
**Wrote:** `test_rover_reports_the_position_and_heading_it_was_created_with`
— fails with `ModuleNotFoundError: No module named 'mars_rover'` at
collection, so the whole test file errors.
**Interface decided:** module `mars_rover`; class `Rover`; constructed as
`Rover(width=, height=, x=, y=, heading=)` with heading a string, one of
`"N"`, `"E"`, `"S"`, `"W"`; readable attributes `x`, `y`, `heading`.
Nothing yet says how obstacles reach the rover. Run the suite with
`.venv/bin/pytest` — pytest is not on the system python; the venv is
gitignored, so `python3 -m venv .venv && .venv/bin/pip install pytest`
if it is missing.
**List:** checked off "The rover is created with a planet `width` columns by
`height` rows, a position, and a heading, and can report its position and
heading". Nothing added.
**Surprise:** none — but writing the list made one silence loud. The task
says the planet has obstacles and the rover is not told where they are,
so something other than the rover has to hold them, and no sentence in
the task says what. The starter test deliberately does not settle it.

## Turn 2 — pong — Tue Sep  1 21:07:57 UTC 2026

**Received:** `test_rover_reports_the_position_and_heading_it_was_created_with`
failing at collection with `ModuleNotFoundError: No module named
'mars_rover'`. The test file was untracked, so it went into my commit.
**Green by:** Obvious Implementation — a constructor that keeps what it is
handed is not something I need to fake.
**Refactored:** nothing to remove. But I did take something out: my first
green stored `width` and `height` as attributes too, and no test asks for
them, so I deleted those two lines. The constructor still accepts them
because the test passes them by keyword.
**Commit:** 7594d0e
**Also satisfied:** none
**Wrote:** `test_moving_forward_facing_north_raises_latitude_by_one` — fails
with `AttributeError: 'Rover' object has no attribute 'execute'`.
**Interface decided:** commands arrive as a string through a method named
`execute`, called for its effect; the test reads the result off `x`, `y`,
`heading` as before, so `execute` is not asked to return anything yet.
**List:** checked off "`F` moves one square forward in the current heading".
Nothing added. I did not check off "`y` runs north" — one test at one
heading does not show that south lowers `y`.
**Surprise:** the width and height the starter test hands over are the two
values that make this planet a planet, and nothing in the suite can see
them yet. They are held in the constructor's signature and dropped on the
floor, and the suite is entirely happy. The first test that wraps will
have to put them back.

## Turn 3 — ping — Tue Sep  1 21:09:12 UTC 2026

**Received:** `test_moving_forward_facing_north_raises_latitude_by_one`
failing with `AttributeError: 'Rover' object has no attribute 'execute'`.
**Green by:** Obvious Implementation — `execute` raises `y` by one. I am
sure that is the real code for the north case, so I did not fake it to a
constant. Both the heading and the letter in the command string are
ignored, because no test demands either yet.
**Refactored:** nothing. There is no constant in the code duplicating a
value in the test — the `1` is the behavior, not the example.
**Commit:** 1d12d7b. I also started tracking `.real-tdd/journal.md` in it;
it was untracked and the run's data should not live only in a working
tree. `.real-tdd/baton` I left untracked on purpose — its value is
meaningless once the turn is over.
**Also satisfied:** none
**Wrote:** `test_moving_forward_facing_south_lowers_latitude_by_one` —
fails with `AssertionError: assert (3, 3, 'S') == (3, 1, 'S')`. The rover
went north while facing south, because `execute` still does not read the
heading.
**Interface decided:** none. Same `execute(commands)` and same three
attributes.
**List:** checked off "`y` runs north: moving north raises `y`, moving
south lowers it" — its north half was already shown, this is the south
half. Nothing added.
**Surprise:** none, but the choice of test was deliberate rather than
obvious. `L` and `R` were closer to hand on the list. I picked the
opposite end of the same axis instead, N against S, because a second
example on a *different* axis — `F` facing east — would not force the
heading to be read; it could be passed by another ignore-the-heading
special case. Two points on one axis is the pair that cannot be faked.

## Turn 4 — pong — Tue Sep  1 21:10:18 UTC 2026

**Received:** `test_moving_forward_facing_south_lowers_latitude_by_one`
failing with `AssertionError: assert (3, 3, 'S') == (3, 1, 'S')` — the rover
moved north while facing south.
**Green by:** Triangulate — two examples at the ends of the same axis, so I
replaced the literal `1` with a lookup on the heading,
`LATITUDE_STEP = {"N": 1, "S": -1}`. The table has two entries and not four:
nothing yet asks what `F` does facing east, and a `KeyError` there is a
truer answer than a wrong number.
**Refactored:** nothing beyond that. The generalization was the green.
**Commit:** a65ab49 — includes your Turn 3 journal and test-list edits,
which were still uncommitted.
**Also satisfied:** none
**Wrote:** `test_turning_left_from_north_faces_west_without_moving` — fails
with `AssertionError: assert (3, 3, 'N') == (3, 2, 'W')`. Two things are
wrong at once and that is the point: the heading did not turn, and the
rover moved north anyway.
**Interface decided:** none. Same `execute(commands)`.
**List:** checked off "`L` turns left ninety degrees". Nothing added.
**Surprise:** `execute` has never once looked at the string it is given.
Three green tests and the argument is still dead — `execute("")` would
walk the rover north. I picked `L` over the east/west axis for that
reason: the axis tests would have gone green with the command string
still unread.

## Turn 5 — ping — Tue Sep  1 21:11:31 UTC 2026

**Received:** `test_turning_left_from_north_faces_west_without_moving`
failing with `AssertionError: assert (3, 3, 'N') == (3, 2, 'W')` — the
heading did not turn and the rover moved anyway.
**Green by:** Fake It — `execute` now loops over the command string and
branches on the letter, but `L` sets the heading to the constant `"W"`,
which is the value the one test expects. I know the real code is a
rotation table; I did not write it because one example cannot tell a
rotation from a constant.
**Refactored:** nothing. The duplication between `"W"` in the code and
`"W"` in the test is real and deliberate — it is what the next test
removes.
**Commit:** 0f17c5a
**Also satisfied:** none. The loop makes "a string of commands is executed
in order" *look* satisfied, and I did not check it off: every test still
passes a one-character string, so the loop could run the commands
backwards and the suite would not notice. That item still needs its test.
**Wrote:** `test_turning_left_from_west_faces_south` — fails with
`AssertionError: assert (3, 2, 'W') == (3, 2, 'S')`. The faked constant
answers `W` to every left turn.
**Interface decided:** none.
**List:** nothing checked, nothing added. This test triangulates "`L` turns
left ninety degrees", which was already checked off after one example —
the item was true of the list before it was true of the code.
**Surprise:** the `else` branch. `execute` treats every letter that is not
`L` as a move, so `execute("Q")` walks the rover north and `execute("R")`
does too. No test forbids it, so it stays, but the suite currently
asserts less than it looks like it does — four green tests and the only
letter the code really knows is `L`.

## Turn 6 — pong — Tue Sep  1 21:12:24 UTC 2026

**Received:** `test_turning_left_from_west_faces_south` failing with
`AssertionError: assert (3, 2, 'W') == (3, 2, 'S')` — the faked `"W"`
answered every left turn.
**Green by:** Triangulate — the constant became `LEFT_OF = {"N": "W",
"W": "S"}`. Two entries, not four, for the same reason `LATITUDE_STEP` has
two: no test turns left from `S` or `E`, and a `KeyError` is a more honest
answer than a guess that happens to be right.
**Refactored:** nothing. Replacing the constant with the lookup was the
green; there was nothing left over.
**Commit:** bc5e030
**Also satisfied:** none
**Wrote:** `test_moving_forward_facing_east_raises_longitude_by_one` —
fails with `KeyError: 'E'` raised inside `execute`, because the only axis
the code can move along is latitude.
**Interface decided:** none.
**List:** nothing checked. "`x` runs east: moving east raises `x`, moving
west lowers it" stays open — this is its east half only, the same way the
north test alone did not close the `y` item.
**Surprise:** the else-branch you flagged is louder from this side. I could
not write a test for "a string of commands is executed in order" without it
going green on arrival — `execute("LL")` already works — so the loop you
wrote is real behavior that no test demands and no test can currently
falsify. I left the item unchecked and picked a different axis instead.

## Turn 7 — ping — Tue Sep  1 21:13:26 UTC 2026

**Received:** `test_moving_forward_facing_east_raises_longitude_by_one`
failing with `KeyError: 'E'` from `LATITUDE_STEP[self.heading]`.
**Green by:** Obvious Implementation — an `if self.heading == "E":
self.x += 1` special case, which is the fastest green and deliberately
ugly.
**Refactored:** the ugliness. The special case meant the code stepped the
two axes in two different shapes, one a table and one a literal. Both are
now one table, `FORWARD_STEP = {"N": (0, 1), "S": (0, -1), "E": (1, 0)}`,
and `execute` adds the pair. Three entries, no `W` — same discipline as
before. Suite green after each of the two edits.
**Commit:** 519d9fb
**Also satisfied:** none. "`x` runs east" is still open; this is only its
east half.
**Wrote:** `test_turning_right_from_north_faces_east_without_moving` —
fails with `AssertionError: assert (3, 3, 'N') == (3, 2, 'E')`.
**Interface decided:** none.
**List:** checked off "`R` turns right ninety degrees". Nothing added.
**Surprise:** the failure message is the surprise, and it is the one we
have both been circling. `R` did not fail with a `KeyError` or by leaving
the heading alone — it moved the rover a square north. The `else` branch
means the rover's answer to a letter it has never heard of is to walk
forward, and this is the first test that says so out loud. Once it is
green, `execute("FR")` and `execute("RF")` will finally differ, and the
order item becomes testable.

## Turn 8 — pong — Tue Sep  1 21:14:29 UTC 2026

**Received:** `test_turning_right_from_north_faces_east_without_moving`
failing with `AssertionError: assert (3, 3, 'N') == (3, 2, 'E')` — `R` fell
through to the else branch and walked north.
**Green by:** Fake It — `elif command == "R": self.heading = "E"`, a
constant, exactly as you faked `L` two turns ago. One example cannot tell a
rotation from a constant, and I am not going to pretend it can.
**Refactored:** nothing. The fake is the duplication and it is deliberate.
**Commit:** baef79a
**Also satisfied:** none
**Wrote:** two tests this turn, which needs explaining.
`test_commands_are_executed_in_the_order_given` — `execute("RF")` from north
lands at `(4, 2, "E")`, and it **passed on arrival**. You called this last
turn: once `R` stopped being a move, `RF` and `FR` finally differ. It
records behavior the loop already had, so by the turn's own rule it is a
Regression Test, not a step, and I picked another item for the red.
The red is `test_turning_left_four_times_returns_to_the_original_heading` —
fails with `KeyError: 'S'`, because `LEFT_OF` runs out after two entries.
**Interface decided:** none.
**List:** checked off "A string of commands is executed in order" (by the
regression test) and "Turning left four times returns the rover to its
original heading", marked left-half-only — the right half needs `R` to stop
being a constant first. Nothing added.
**Surprise:** the two-entry tables have started to bite. Every table we have
built — `FORWARD_STEP`, `LEFT_OF` — is a partial function, and the suite
grew for six turns without noticing, because every test we wrote stayed
inside the entries that existed. `LLLL` is the first test that walks off the
end of one, and it does it not by asserting anything new but by repeating a
command we already have four times.

## Turn 9 — ping — Tue Sep  1 21:15:36 UTC 2026

**Received:** `test_turning_left_four_times_returns_to_the_original_heading`
failing with `KeyError: 'S'` — `LEFT_OF` ran out after two entries.
**Green by:** Obvious Implementation — `LEFT_OF` became the complete cycle,
`{"N": "W", "W": "S", "S": "E", "E": "N"}`. This is not me abandoning the
two-entry discipline: four lefts from north visit all four headings, so
every entry I added is one the test walks through.
**Refactored:** nothing. I looked at folding `LEFT_OF` and the still-faked
`"E"` in the `R` branch into one ordered compass, and did not: `R` has one
example behind it and turning that fake into a rotation would be adding
behavior no test asks for. It is your fake to remove.
**Commit:** 8b4a106
**Also satisfied:** none
**Wrote:** `test_moving_east_off_the_last_column_lands_on_column_zero` —
`Rover(width=10, ..., x=9, heading="E")` then `F`. Fails with
`AssertionError: assert (10, 2, 'E') == (0, 2, 'E')`. The rover walked off
the edge of the map onto column 10, which does not exist.
**Interface decided:** none. The constructor already takes `width`.
**List:** checked off "Longitude wraps: moving east off the last column
lands on column 0". Nothing added.
**Surprise:** none in the code, but this is the test you predicted on
turn 2. `width` has been accepted and dropped on the floor for eight
turns, and the suite has been fully green the whole time with the rover
living on an infinite plane. Column 10 on a ten-column planet is the first
assertion that has ever needed the planet to have a size.

## Turn 10 — pong — Tue Sep  1 21:16:39 UTC 2026

**Received:** `test_moving_east_off_the_last_column_lands_on_column_zero`
failing with `AssertionError: assert (10, 2, 'E') == (0, 2, 'E')`.
**Green by:** Obvious Implementation — `self.width` finally kept in the
constructor, and the eastward step became `(self.x + step_x) % self.width`.
Modulo is one operation, not two, so I did not try to write an
east-only version of it.
**Refactored:** nothing.
**Commit:** f140775
**Also satisfied:** none — and this is the interesting one to be careful
about. That `% self.width` makes the *west* wrap work too, and there is no
test for it, so I did not check the item off. The behavior is there by
accident of the operator, not because a test drove it.
**Wrote:** `test_turning_right_from_east_faces_south` — fails with
`AssertionError: assert (3, 2, 'E') == (3, 2, 'S')`, the faked constant
answering `E` again.
**Interface decided:** none.
**List:** nothing checked, nothing added.
**Surprise:** I nearly wrote `RRRR` instead — it is the item on the list and
it mirrors your `LLLL` — and then noticed it does not force what it looks
like it forces. A two-entry table `{"N": "E", "E": "N"}` passes both `RRRR`
and the existing right-turn test, because four steps of a two-cycle also
land where they started. `LLLL` had the same hole; you filled it with the
whole compass, which the test never actually demanded. So I took the
smaller step instead: two examples that share no entry.

## Turn 11 — ping — Tue Sep  1 21:17:45 UTC 2026

**Received:** `test_turning_right_from_east_faces_south` failing with
`AssertionError: assert (3, 2, 'E') == (3, 2, 'S')` — the faked `"E"`.
**Green by:** Triangulate — the constant became `RIGHT_OF = {"N": "E",
"E": "S"}`, two entries sharing no key with each other, exactly the pair
you chose.
**Refactored:** the second compass. Two hand-written tables were encoding
one fact — `LEFT_OF["S"] == "E"` and `RIGHT_OF["E"] == "S"` are the same
sentence read in two directions — so `RIGHT_OF` is now derived,
`{left: heading for heading, left in LEFT_OF.items()}`. Suite green after
the green and again after the refactor.
**Commit:** 7230636
**Also satisfied:** "Turning left four times returns the rover to its
original heading; likewise turning right" — the right half now works,
because inverting a complete cycle gives a complete cycle. I did **not**
check it off. This is your `% self.width` again: the behavior arrived as a
property of the operation, not because a test asked for it, and `RRRR`
still deserves its test. Noted here so it is not mistaken for driven.
**Wrote:** `test_moving_backward_facing_north_lowers_latitude_by_one` —
fails with `AssertionError: assert (3, 3, 'N') == (3, 1, 'N')`.
**Interface decided:** none.
**List:** checked off "`B` moves one square backward". Nothing added.
**Surprise:** the refactor was a judgement call and I want it on the
record as one. Deriving `RIGHT_OF` removes real duplication, but it also
hands the rover two heading transitions no test has ever asked for, which
is the thing we have spent eleven turns refusing to do by hand. I took it
because it is the same trade you took with modulo — free behavior that
falls out of the right operation — and because the alternative was
keeping two copies of the compass and grinding out `R` from `S` and `W`
one example at a time. The rule we seem to be converging on: behavior may
arrive free from an operation, but never from a guess, and either way the
list item stays open until a test pins it.

## Turn 12 — pong — Tue Sep  1 21:18:55 UTC 2026

**Received:** `test_moving_backward_facing_north_lowers_latitude_by_one`
failing with `AssertionError: assert (3, 3, 'N') == (3, 1, 'N')` — `B` fell
into the else branch and moved forward.
**Green by:** Obvious Implementation — a `B` branch that steps the negated
forward step. I wrote it as a copy of the `F` code on purpose, to get green
in one edit and let the refactor deal with the mess.
**Refactored:** the two copies of the move. There is now one `_move(sign)`
with `MOVE_SIGN = {"F": 1, "B": -1}`, and the branch reads
`self._move(MOVE_SIGN[command])`. Suite green after the green and after the
refactor.

One consequence to declare rather than bury: the else branch is no longer a
catch-all. `execute("Q")` used to walk the rover north and now raises
`KeyError: 'Q'`. No test asserted the old behavior and none asserts the new
one — I removed a wart we had both flagged, and I am not claiming a test
drove it.
**Commit:** 045ba73
**Also satisfied:** none
**Wrote:** `test_moving_forward_facing_west_lowers_longitude_by_one` — fails
with `KeyError: 'W'` from `FORWARD_STEP`.
**Interface decided:** none.
**List:** checked off "`x` runs east: moving east raises `x`, moving west
lowers it" — this is its west half. Nothing added.
**Surprise:** `FORWARD_STEP` has been missing `W` since turn 7, and the
rover has driven backward, wrapped around the planet and turned through the
whole compass without once noticing it cannot go west. Your derived
`RIGHT_OF` is what finally exposed it: `R` from `S` now answers `W`, so the
suite can reach a heading the movement table has never had an entry for.
Twelve turns in, the rover can face a direction it cannot walk in.

## Turn 13 — ping — Tue Sep  1 21:20:12 UTC 2026

**Received:** `test_moving_forward_facing_west_lowers_longitude_by_one`
failing with `KeyError: 'W'` from `FORWARD_STEP`.
**Green by:** Obvious Implementation — `"W": (-1, 0)`. The table is now
total on the compass.
**Refactored:** nothing. I looked for duplication between `FORWARD_STEP`
and `LEFT_OF` — both are keyed by heading — and there is none worth
removing; one is a vector and one is a rotation.
**Commit:** fcfe970, and a second commit 0e8022e explained below.
**Also satisfied:** none
**Wrote:** two tests, and the first one is not a step.
`test_moving_west_off_column_zero_lands_on_the_last_column` **passed on
arrival**, exactly as you predicted on turn 10 — `% self.width` had the
reverse wrap all along, it just needed the `W` entry to be reachable. So
it is a Regression Test. I committed it on its own (0e8022e) rather than
leaving it in the working tree, so that what you receive is one failing
test and nothing else.
The red is `test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was` —
fails with `TypeError: Rover.__init__() got an unexpected keyword
argument 'obstacles'`.
**Interface decided:** obstacles reach the rover through a keyword
argument on the constructor, `obstacles=[(3, 3)]`, a collection of
`(x, y)` pairs. Existing tests do not pass it, so it needs a default.
**List:** checked off "Longitude wraps in reverse" (by the regression
test) and "A move that would land on an obstacle leaves the rover where it
was". Nothing added.
**Surprise:** the interface decision was the hard part of this turn and I
want the reasoning on the record, because I nearly went the other way.
Twist 2 says the rover is not told where the obstacles are, and my first
instinct was a separate `Planet(width, height, obstacles)` that the rover
is handed — the task's own words are "the planet has obstacles". I did not
write that test. It would have rewritten the constructor call in fourteen
tests as the price of one new behavior, and it would have been me
designing the object graph in advance of any pressure to have one. So the
rover now takes `width`, `height` **and** `obstacles` — three arguments
that all describe the planet and none that describe the rover. That is a
duplication with a name waiting for it, and if it starts to hurt, the
extraction will be driven rather than planned. The constructor argument is
the world's truth, not the rover's map; the map is still empty and Twist 2
has not started.

## Turn 14 — pong — Tue Sep  1 21:21:01 UTC 2026

**Received:** `test_a_move_onto_an_obstacle_leaves_the_rover_where_it_was`
failing with `TypeError: Rover.__init__() got an unexpected keyword argument
'obstacles'`.
**Green by:** Obvious Implementation — `obstacles=()` on the constructor, and
`_move` now computes the target square first and returns without assigning if
that square is an obstacle. The default is an empty tuple so the other
fourteen tests keep their call.
**Refactored:** nothing, though the shape shifted a little to get there:
`_move` had been assigning `self.x` and `self.y` as it computed them, and it
cannot decide whether to move until it knows the whole square, so the two
assignments became one `self.x, self.y = square`.
**Commit:** 8a9b126
**Also satisfied:** none
**Wrote:** `test_a_move_blocked_by_an_obstacle_abandons_the_rest_of_the_commands`
— `execute("FR")` into an obstacle. Fails on the heading: `'E' != 'N'`. The
blocked `F` did nothing, and then the `R` ran anyway.
**Interface decided:** none. I took your `obstacles=` as given.
**List:** checked off "A move blocked by an obstacle abandons the rest of the
command string". Nothing added.
**Surprise:** the assertion that caught this is the one I have written in
every test without thinking — the full `(x, y, heading)` triple. The
positional half of it is identical to the previous test and says nothing new;
the rover was never going to move. It is the heading, dragged along for
fourteen turns as boilerplate, that fails. If I had asserted only "the rover
did not move" the suite would have gone green on a rover that keeps executing
commands after it crashes into a rock.

## Turn 15 — ping — Tue Sep  1 21:21:51 UTC 2026

**Received:**
`test_a_move_blocked_by_an_obstacle_abandons_the_rest_of_the_commands`
failing with `AssertionError: assert (3, 2, 'E') == (3, 2, 'N')` — the
blocked `F` did nothing and the `R` ran anyway.
**Green by:** Obvious Implementation — `_move` returns whether it moved,
and `execute` returns when it did not. A boolean, not the obstacle: no
test asks which one yet, and that is the next test.
**Refactored:** nothing.
**Commit:** 41cfc97
**Also satisfied:** none
**Wrote:** `test_after_a_blocked_command_string_the_rover_reports_which_obstacle`
— fails with `AttributeError: 'Rover' object has no attribute
'blocked_by'`.
**Interface decided:** the rover reports the obstacle through an attribute
`blocked_by`, holding the `(x, y)` square. This test only fixes what it
holds after a block; what it holds after a clean run is the next item on
the list and I have deliberately not decided it here.
**List:** checked off "After a blocked command string the rover reports
that it stopped because of an obstacle, and which one". Nothing added.
**Surprise:** your point about the `(x, y, heading)` triple has a second
half I noticed while writing this test. The triple has been doing free
work for fifteen turns, but it cannot do this one — there is no way to
spell "stopped because of a rock" in three fields that describe where the
rover is. This is the first test in the run whose assertion is not the
triple, and the first behavior the rover has that is about its history
rather than its state.

## Turn 16 — pong — Tue Sep  1 21:22:43 UTC 2026

**Received:**
`test_after_a_blocked_command_string_the_rover_reports_which_obstacle`
failing with `AttributeError: 'Rover' object has no attribute 'blocked_by'`.
**Green by:** Obvious Implementation — one line, `self.blocked_by = square`
where `_move` decides not to move. I did **not** initialise `blocked_by` in
the constructor. Nothing tests what it holds before a block, so right now the
attribute springs into existence the first time the rover hits a rock, which
is indefensible as design and exactly what the tests demand.
**Refactored:** nothing. `_move` now says "blocked" twice, once by setting
`blocked_by` and once by returning `False`, and I left the pair alone: the
boolean is what `execute` reads and the attribute is what the test reads, and
I would rather the next test tell us which one survives.
**Commit:** dcaab4c
**Also satisfied:** none
**Wrote:** `test_after_an_unblocked_command_string_no_obstacle_is_reported` —
a rover whose obstacle is far away at `(7, 7)` moves one square and is asked
what blocked it. Fails with the same `AttributeError`, which is the point:
the attribute I just wrote does not exist yet on a rover that has never
crashed.
**Interface decided:** `blocked_by` is `None` when nothing blocked the run.
Your test fixed what it holds after a block; this one fixes the other half.
**List:** checked off "After a command string that was not blocked the rover
reports that it did not stop because of an obstacle". Added one item I do not
think either of us had seen: "A rover that was blocked, and then runs a
command string that is not blocked, no longer reports an obstacle." Neither
test covers it — mine starts from a clean rover — and `blocked_by` is written
once and never cleared, so a rover that hits a rock currently reports that
rock forever.
**Surprise:** writing a test for "nothing went wrong" found a bug in the code
I wrote ninety seconds earlier, and not the bug the test was about. The
missing initialiser is a `None` away from fixed. The stale report is not, and
it only became visible because the report is now something the rover carries
between command strings rather than something it computes.

## Turn 17 — ping — Tue Sep  1 21:23:44 UTC 2026

**Received:** `test_after_an_unblocked_command_string_no_obstacle_is_reported`
failing with `AttributeError: 'Rover' object has no attribute 'blocked_by'`
— the attribute only existed on a rover that had already crashed.
**Green by:** Obvious Implementation — `self.blocked_by = None` in the
constructor.
**Refactored:** the double signal you left for the next test to settle.
`_move` now answers with the obstacle that stopped it, or `None`, and
`execute` records it and returns. The boolean is gone. You were right not
to guess which one survives — it turned out to be neither: the return
value became the obstacle, and the attribute became the thing `execute`
writes, so the two "blocked" statements collapsed into one that travels
from `_move` to `execute` to the report.
**Commit:** 18cac75
**Also satisfied:** none
**Wrote:** `test_a_later_unblocked_command_string_clears_the_obstacle_report`
— the item you added. A rover hits `(3, 3)`, then runs `"RF"`, which turns
and moves into open ground. Fails with `assert (3, 3) is None`: the rover
is still reporting a rock it drove away from. I used `"RF"` rather than a
bare turn so that the string that clears the report contains a move that
actually succeeds.
**Interface decided:** none.
**List:** checked off "A rover that was blocked, and then runs a command
string that is not blocked, no longer reports an obstacle". Nothing added.
**Surprise:** none for me — you found this one and wrote it down, and all
I did was collect it. Worth recording that the list caught it: the item
existed for one turn before the test did, which is the only reason the
bug survived your turn without being lost.

## Turn 18 — pong — Tue Sep  1 21:24:47 UTC 2026

**Received:** `test_a_later_unblocked_command_string_clears_the_obstacle_report`
failing with `assert (3, 3) is None` — the rover still naming a rock it had
driven away from.
**Green by:** Obvious Implementation — `execute` sets `self.blocked_by = None`
before the loop. The report is now about the command string just run, not
about the rover's whole life.
**Refactored:** nothing. The constructor also sets `blocked_by = None` and I
kept it: it is not the same statement as the reset, it is what makes the
attribute exist on a rover that has never been given a command.
**Commit:** ed926fb
**Also satisfied:** none
**Wrote:** three tests, two of which are not steps. The classic part had two
items left and **both passed on arrival**:
`test_an_empty_command_string_leaves_the_rover_where_it_was` and
`test_turning_to_face_an_obstacle_is_not_blocked`. Regression tests, kept for
what they forbid rather than what they added — nothing in the code says
turning ignores obstacles, it is true only because the `L` and `R` branches
never reach `_move`, and now something says it.
The red is `test_moving_north_off_the_north_pole_row_stays_on_that_row` —
`Rover(height=6, y=5, heading="N")` runs `F` and fails with `assert 6 == 5`.
The rover walked off the top of the map onto a row that does not exist.
**Interface decided:** none.
**List:** checked off "An empty command string leaves the rover where it was",
"Turning never hits anything, even facing an obstacle" (both by regression
test) and "Moving north from the north pole row does not wrap to the south
pole row". The classic part is now closed. Nothing added.
**Surprise:** `height` has been accepted and dropped on the floor for
eighteen turns — the same silence `width` sat in until turn 10, and I said
then that the first test to wrap would put it back. It was not a wrapping
test that put `height` back. It is a test about a place where the map
deliberately does *not* wrap. I split the pole crossing into its three list
items on purpose and this test asserts only `rover.y`, not the triple: the
longitude and the heading are the next two tests, and asserting them now
would have handed you a step three behaviors wide.

## Turn 19 — ping — Tue Sep  1 21:25:35 UTC 2026

**Received:** `test_moving_north_off_the_north_pole_row_stays_on_that_row`
failing with `assert 6 == 5` — the rover on row 6 of a six-row planet.
**Green by:** Obvious Implementation — `self.height` kept at last, and the
new latitude discarded when it leaves the map: `if y >= self.height: y =
self.y`. Only the north side. There is no `y < 0` clause, because no test
goes south off the bottom yet and the south pole is still an open item.
**Refactored:** nothing.
**Commit:** 88ac39f
**Also satisfied:** none. The rover now stays on the pole row but does not
cross the pole — it just stops, which is not what the task says happens
and is exactly as much as the test asked for.
**Wrote:** `test_crossing_the_north_pole_puts_the_rover_on_the_far_side` —
`width=10`, so half a planet is five columns; from `x=3` on the pole row,
`F` should land on `x=8`. Fails with `assert 3 == 8`. The rover held its
longitude and went nowhere.
**Interface decided:** none.
**List:** checked off "Crossing the north pole puts the rover at longitude
`x + width / 2` modulo `width`". Nothing added.
**Surprise:** the green I wrote is a lie that passes, and I left it in on
purpose. A rover that stops dead at the pole satisfies the test you wrote
and contradicts the task, which says it crosses. The one-behavior-per-test
split you made is what produced that: each of the three assertions about
the pole is individually satisfiable by something that is not a pole
crossing. It takes all three to force the real thing, and until they are
all in, the code is allowed to be wrong in a way both of us can read on
the page. That is uncomfortable to hand over and I think it is the method
working rather than failing.

## Turn 20 — pong — Tue Sep  1 21:26:18 UTC 2026

**Received:** `test_crossing_the_north_pole_puts_the_rover_on_the_far_side`
failing with `assert 3 == 8` — the rover held its longitude and stopped at the
pole.
**Green by:** Obvious Implementation — the longitude is now computed alongside
the latitude, and the branch that keeps the rover on the pole row adds
`self.width // 2` to it. Integer division, because the task promises `width` is
even and nothing in the code has an opinion about half a column.
**Refactored:** nothing. `_move` is getting crowded — three lines of ordinary
stepping and then a special case that rewrites both of them — but the third
pole test is not in yet and I would rather refactor once the shape is settled
than twice.
**Commit:** 886956c
**Also satisfied:** none
**Wrote:** `test_crossing_the_north_pole_turns_the_rover_south` — fails with
`assert 'N' == 'S'`. This is the third of the three you flagged last turn.
**Interface decided:** none.
**List:** checked off "Crossing the north pole leaves the rover heading south".
Nothing added.
**Surprise:** your "green that is a lie" is now half a lie, and this test is
what makes the difference legible. After my green the rover teleports across
the pole and keeps facing north, which is a rover walking backwards up the map
— and the suite is green, because between us we had asserted where it lands
but never which way it ends up pointing. The uncomfortable thing you handed me
was not that a fake passed. It is that a *partly real* implementation looks
exactly like a finished one from inside the suite, and only the list says
otherwise. Three items, three assertions, and the honesty of the code is
carried by the item that has not been checked off yet.

## Turn 21 — ping — Tue Sep  1 21:27:25 UTC 2026

**Received:** `test_crossing_the_north_pole_turns_the_rover_south` failing
with `assert 'N' == 'S'` — the rover teleporting across the pole and still
facing north.
**Green by:** Obvious Implementation — a `crosses_pole` flag, and
`self.heading = "S"` after the move is taken. The constant, not a
reversal: one pole is one example.
**Refactored:** yes, the crowding you decided to leave. `crosses_pole` was
being tested twice, once to bend the square and once to bend the heading,
and the two halves of one fact had drifted to opposite ends of the method
with the obstacle check between them. A move now has a destination that
is a square *and* a heading, computed together by `_destination(sign)`;
`_move` asks where the move would put the rover and decides whether to
take it. The pole is one branch in one place, and the ordinary case
returns `self.heading` unchanged, so nothing else in the suite noticed.
Green after the green and again after the refactor.
**Commit:** 4885cea
**Also satisfied:** none
**Wrote:** `test_moving_south_off_the_south_pole_row_crosses_the_south_pole`
— fails with `AssertionError: assert (3, -1, 'S') == (8, 0, 'N')`. Row
minus one, and the rover is now off the bottom of the map.
**Interface decided:** none.
**List:** checked off "Moving south from the south pole row crosses the
south pole, mirrored". Nothing added.
**Surprise:** I did not split this one into three the way you split the
north, and the reason is worth recording because it is the opposite call
on the same question. Splitting the north was right when no pole mechanism
existed: three narrow tests each admitted a cheap wrong answer, and that
was visible and temporary. The mechanism exists now, so the south pole is
one generalization rather than three behaviors — the task states it in one
sentence, "the same happens at the south pole row, mirrored", and I made
the test that sentence. It also means the failure you receive is honest
about the size of the step: `(3, -1, 'S')` against `(8, 0, 'N')` shows all
three things wrong at once, which is what a missing mirror actually looks
like.

## Turn 22 — pong — Tue Sep  1 21:29:14 UTC 2026

**Received:** `test_moving_south_off_the_south_pole_row_crosses_the_south_pole`
failing with `assert (3, -1, 'S') == (8, 0, 'N')` — three things wrong at once,
as you said.
**Green by:** Obvious Implementation — a mirrored `if y < 0` branch returning
the far side and `"N"`, written as a deliberate copy of the north branch.
**Refactored:** the copy, immediately. The two branches differ only in the
heading they name, and that heading is the one the rover already has, flipped:
`BEHIND = {"N": "S", "S": "N"}`. One branch now, guarded by
`not 0 <= y < self.height`. Two entries, and the table is total where it is
used — a rover crossing a pole is by definition moving along latitude. Suite
green after the green and after the refactor.
**Commit:** a7e71e1
**Also satisfied:** none by that commit, but see below.
**Wrote:** four tests, and only the last is a step. The three remaining Twist 1
items **all passed on arrival**:
`test_backing_off_the_north_pole_row_crosses_the_pole`,
`test_backing_off_the_south_pole_row_crosses_the_pole`, and
`test_an_obstacle_on_the_far_side_of_the_pole_blocks_the_crossing`. Regression
tests, all three. Twist 1 is closed.
The red is `test_a_new_rover_has_discovered_no_obstacles` — fails with
`AttributeError: 'Rover' object has no attribute 'discovered'`.
**Interface decided:** the rover reports what it has learned through an
attribute `discovered`, a list of `(x, y)` squares. A list and not a set,
because the order is part of the behavior; empty on a rover that has bumped
into nothing.
**List:** checked off the three Twist 1 items above and "A new rover has
discovered no obstacles". Nothing added. Nine items left, all Twist 2.
**Surprise:** one of those regressions is not free and I want you to check me
on it. "A backward move off the north pole row crosses the pole the same way a
forward move in the opposite heading would" has two readings. Read as *same
resulting state*, a rover on the pole row facing south that reverses over the
pole should end up facing south, because that is where the equivalent forward
rover ends up. Read as *same mechanism*, it ends up facing north — the flip
applies to the heading it actually has. I wrote the test for the second
reading, and the code passed it without being touched.

I chose it on the physics rather than the grammar. The first reading gives a
rover that reverses over the pole and then reverses back over it on the next
`B`, oscillating across the pole forever, because its heading no longer agrees
with the direction it is travelling. The second gives a rover that keeps going.
If you read the task line the other way, hand it back — the assertion is mine
and it is exactly the kind of thing a test should not be allowed to decide
quietly.

## Turn 23 — ping — Tue Sep  1 21:30:14 UTC 2026

**Received:** `test_a_new_rover_has_discovered_no_obstacles` failing with
`AttributeError: 'Rover' object has no attribute 'discovered'`.
**Green by:** Obvious Implementation — `self.discovered = []` in the
constructor.
**Refactored:** nothing.
**Commit:** 72d1189, which also carries your three Twist 1 regression
tests.
**Also satisfied:** none

**On the reading you asked me to check: I agree with you, keep the test.**
Your assertion is the right one and I would have argued for it. The
grammar reading loses on its own consequences. Take a rover on the north
pole row facing south and run `B` twice. Under the *same resulting state*
reading it ends the first `B` at `(8, 5)` still facing south; the second
`B` computes `y = 5 + 1 = 6`, leaves the map again, and it crosses back.
It oscillates across the pole forever, one crossing per command, and it
never travels anywhere. Under your reading it ends facing north, and the
next `B` walks it south down the far side, which is where it was already
going.
The physical reason is that crossing a pole reverses every direction on
the map at once, and the rover has two of them: the way it faces and the
way it travels. A backing rover has them opposed. Flip both and they stay
opposed, so it keeps reversing in a straight line — that is your
`BEHIND[self.heading]`. Flip only the one the task sentence mentions and
they stop disagreeing, which is a rover that changes its mind at the pole.
"The same way" is about the crossing, not about ending where a different
rover would end.

**Wrote:** `test_an_obstacle_the_rover_bumps_into_is_remembered` — fails
with `assert [] == [(3, 3)]`.
**Interface decided:** none. I took your `discovered` list as given.
**List:** checked off "An obstacle the rover bumps into is remembered as
discovered". Nothing added. Eight items left, all Twist 2.
**Surprise:** the rover now has two collections of obstacles and the names
do not distinguish them. `self.obstacles` is the world's truth, which the
rover is not supposed to know, and `self.discovered` is its map, which is
the only thing it is allowed to act on. They are one attribute apart in
the constructor. Every remaining item on the list is about telling them
apart, and the first one that reads `self.obstacles` where it means
`self.discovered` will pass its test and be wrong.

## Turn 24 — pong — Tue Sep  1 21:31:04 UTC 2026

**Received:** `test_an_obstacle_the_rover_bumps_into_is_remembered` failing
with `assert [] == [(3, 3)]`. And thank you for the check on the pole reading —
your two-directions argument is better than the one I had.
**Green by:** Obvious Implementation — one line in `execute`, appending the
obstacle to `discovered` next to where it is already recorded as `blocked_by`.
**Refactored:** nothing.
**Commit:** cc6f11c
**Also satisfied:** none
**Wrote:** `test_bumping_into_the_same_obstacle_twice_records_it_once` — the
same rover runs `F` into the same rock twice. Fails with `assert [(3, 3),
(3, 3)] == [(3, 3)]`.
**Interface decided:** none.
**List:** checked off "Bumping into the same obstacle again does not record it
twice". Nothing added. Seven items left.
**Surprise:** this test cannot fail for the reason it is about, once the next
item lands. It bumps twice, but by the second `F` the rock is *known*, and the
refusal rule says a known collision is refused before the rover moves at all —
so a rover that implements refusal never reaches the recording code a second
time and the test passes for a reason that has nothing to do with duplicates.
Right now there is no refusal, so it fails honestly and the fix is a real
guard. I am handing over a test whose failure is genuine today and whose
meaning changes underneath it in a few turns. I could not find a way to write
the duplicate rule that does not have this property: the two rules overlap on
every input where either is observable.

## Turn 25 — ping — Tue Sep  1 21:32:29 UTC 2026

**Received:** `test_bumping_into_the_same_obstacle_twice_records_it_once`
failing with `assert [(3, 3), (3, 3)] == [(3, 3)]`.
**Green by:** Obvious Implementation — `if obstacle not in self.discovered`
around the append.
**Refactored:** nothing.
**Commit:** 38394b3, and 871b670 explained below.
**Also satisfied:** none
**Wrote:** two tests, the first not a step.
`test_discovered_obstacles_are_reported_in_the_order_they_were_found`
**passed on arrival** — a rover bumps `(3, 3)`, turns east, bumps
`(4, 2)`, and the list holds them in that order because it is a list.
Regression Test, committed on its own (871b670).
The red is
`test_a_command_string_that_would_hit_a_known_obstacle_is_refused_as_a_whole`
— fails with `AssertionError: assert (3, 2, 'N') == (3, 1, 'N')`.
**Interface decided:** none.
**List:** checked off "The rover reports discovered obstacles in the order
it discovered them" (by regression test) and "A command string that would
bump into an obstacle the rover already knows about is refused as a whole:
the rover does not move at all". Five items left.
**Surprise:** writing this red took three attempts, and the difficulty is
the interesting part. Refusal and bumping are indistinguishable on almost
every input. If the known rock is one square ahead, both rules leave the
rover exactly where it stands, and the test passes on a rover that has
never heard of refusal. The behavior only becomes visible when the rover
would have travelled *before* it hit — so the test drives three squares
north to learn the rock the classic way, backs one square off it, and then
asks for two forward. A bumping rover ends on `(3, 2)`, one square gained
and stopped at the rock. A refusing rover never leaves `(3, 1)`. The
single square between those two positions is the whole of Twist 2's first
half, and no shorter arrangement shows it.

On your point from last turn: I think it is the same shape. Your duplicate
test will be passed by the refusal guard for the wrong reason, and my
refusal test needs a rover that has already bumped. The two rules do not
just overlap on their inputs — each one hides the other's evidence.

## Turn 26 — pong — Tue Sep  1 21:34:27 UTC 2026

**Received:**
`test_a_command_string_that_would_hit_a_known_obstacle_is_refused_as_a_whole`
failing with `assert (3, 2, 'N') == (3, 1, 'N')` — the rover gained the one
square that separates bumping from refusing. Your three attempts to find that
square were worth it; the test could not have been shorter.
**Green by:** Obvious Implementation — `execute` walks the command string
against `self.discovered` before it moves, and returns if the walk hits
anything. I wrote the walk as a straight copy of the movement geometry, which
made the file briefly contain two rovers.
**Refactored:** that copy, and it took the whole shape of the class with it.
There is now one stepping function, `_after(x, y, heading, command)`, that
answers where a single command would put a rover — pure, no `self` state
touched — and two callers that differ only in what they do with the answer:
`_first_obstacle_on` walks the string and reports, `execute` walks it and
commits. `_move` and `_destination` are gone. Suite green after the green and
after the refactor.

One thing I dropped rather than kept: `execute` no longer asks whether the
command was a move before checking the destination against the obstacles.
A turn returns the square the rover is already standing on, and a rover is
never standing on an obstacle, so the check is a no-op for turns. Your
regression test for "turning never hits anything" is what let me remove the
guard and know it.
**Commit:** d0f8810
**Also satisfied:** none
**Wrote:** `test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit`
— your arrangement again, asserting the report instead of the position. Fails
with `assert None == (3, 3)`: the refusal clears `blocked_by` and then returns
without ever saying why.
**Interface decided:** none. The refusal reports through the same `blocked_by`
as a bump.
**List:** checked off "After refusing a command string the rover reports which
known obstacle it would have hit". Four items left.
**Surprise:** the refactor unified two things the task states as opposites.
Twist 2 spends a paragraph distinguishing a known obstacle from an unknown one
— refused in advance versus bumped into — and after the refactor the
difference is one argument: which collection you walk the string against.
`_first_obstacle_on(commands, self.discovered)` is the rover's map and
`self.obstacles` is the world. The two rules are the same walk asking two
different oracles, and the reason they were so hard to tell apart in tests is
that they were never two behaviors.

## Turn 27 — ping — Tue Sep  1 21:37:38 UTC 2026

**Received:**
`test_a_refused_command_string_reports_the_known_obstacle_it_would_have_hit`
failing with `assert None == (3, 3)` — the refusal returned without saying
why.
**Green by:** Obvious Implementation — the refusal sets `blocked_by` to
what the look-ahead found.
**Refactored:** the report is now one assignment, not two. `execute` used
to clear `blocked_by` and then, separately, set it if the walk found
something; both are `self.blocked_by = self._first_obstacle_on(commands,
self.discovered)`, because that walk answers `None` exactly when there is
nothing to report. Suite green after the green and after the refactor.
**Commit:** e8c717b, and d6641da explained below.
**Also satisfied:** none
**Wrote:** five tests, and **none of them is a step**. Every remaining item
passed on arrival, so all five are Regression Tests, committed together on
green as d6641da:
- `test_a_command_string_is_refused_for_a_known_obstacle_it_would_hit_later_on`
- `test_a_command_string_that_turns_away_from_a_known_obstacle_is_not_refused`
- `test_a_command_string_of_only_turns_is_never_refused`
- `test_a_refused_command_string_discovers_nothing_new`
- `test_a_known_obstacle_reached_only_by_wrapping_is_seen_in_advance`
**Interface decided:** none.
**List:** checked off the four remaining Twist 2 items. Added and checked
off one: "A known obstacle reached only by wrapping round the planet is
seen in advance, like any other" — the wrap half of the avoided-collision
item, which I could not write as an *avoidance* at all, because on a
cylinder every eastward path eventually reaches every column; the real
content is that the look-ahead wraps the same way the movement does.
Also removed the "(left half only)" qualifier from the four-turns item:
`RRRR` in the turn-only test closes the half that had been open since
turn 8. **The list is empty.**

**Surprise:** the run ended without a red. I went looking for one, item by
item, and could not find a behavior left in the task that the code did not
already have — and the reason is your last refactor. Once refusal and
bumping became the same walk asking two different oracles, five separate
sentences of the task collapsed into consequences of one function. A test
for "refused three moves in" cannot fail differently from a test for
"refused one move in" when both are `_first_obstacle_on` with a longer
string. That is the strongest argument for refactoring I have seen in this
run, and also the most uncomfortable: the last five tests could not have
driven anything, and if we had written them first we would have learned
nothing from them.

One thing I am leaving unresolved for the human rather than fixing
quietly. `Rover` is constructed with `width`, `height` and `obstacles` —
three arguments that describe the planet, not the rover — and it carries
`self.obstacles`, the world's truth, next to `self.discovered`, its map.
The tests never let the two be confused, and `_first_obstacle_on` takes
the collection to consult as an argument precisely so the caller must say
which one it means. But Twist 2 says the rover is not told where the
obstacles are, and this rover is holding the list. I flagged it on turn 13
when I chose not to invent a `Planet`, and no test ever pushed back hard
enough to force one. That is either the method being honest about what the
tests demanded, or the method missing something a designer would have
seen on day one. I do not think the journal can settle which, and it seems
worth the human deciding.

**Final state:** 39 tests, all green, 36 list items, all checked. Baton set
to `done`.
