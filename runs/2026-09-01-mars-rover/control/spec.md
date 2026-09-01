---
title: 'Mars rover with spherical poles and obstacle learning'
type: 'feature'
created: '2026-09-01'
status: 'done' # draft | ready-for-dev | in-progress | in-review | done
route: 'dispatch'
review_loop_iteration: 0 # incremented by step-04 before each review loopback
baseline_commit: 'cdfe805cb58f15d380798fe569267a00817e9fb0'
context: ['{project-root}/TASK.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `TASK.md` specifies a Mars rover kata with two departures from the classic exercise: the grid is a sphere, so north/south movement crosses the poles instead of wrapping, and the rover starts with no map, learning obstacles by bumping into them. The repository has no implementation.

**Approach:** One stdlib-only Python package. `Planet` owns the grid geometry and the true obstacle set; `Rover` owns position, heading, and the obstacles it has discovered, and queries the planet only when it actually attempts a move. Pytest suite covering both twists.

## Boundaries & Constraints

**Always:**
- Longitude wraps modulo `width`. Latitude never wraps: leaving a pole row crosses the pole — `y` unchanged, `x -> (x + width // 2) % width`, heading reversed N<->S.
- A blocked move changes nothing — not position, not heading.
- The rover learns obstacles only by attempting a move onto one.
- Discovered obstacles are reported in discovery order, without duplicates.
- Standard library only, plus pytest as a dev dependency.

**Never:**
- Do not let `Rover` enumerate or scan `Planet`'s obstacle set — discovery comes from attempted moves only.
- No CLI, no persistence, no third-party runtime dependencies.
- Do not treat the grid as a torus in the latitude direction.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Behavior |
|----------|--------------|-------------------|
| Longitude wrap | width 10, (9,5) facing E, `"F"` | (0,5) facing E |
| Pole crossing, forward | 10x6, (2,5) facing N, `"F"` | (7,5) facing S |
| Pole crossing, backward | 10x6, (2,5) facing S, `"B"` | (7,5) facing N |
| Pole round trip | north row, `"FB"` | starting square and heading |
| Bump unknown obstacle | obstacle (5,7), at (5,5) facing N, `"FFF"` | stops (5,6), outcome blocked, obstacle (5,7), third command abandoned |
| Learning | after that bump | discovered == [(5,7)] |
| No duplicate learning | bump the same obstacle twice | discovered still == [(5,7)] |
| Refuse known obstacle | (5,7) discovered, at (5,5) facing N, `"RLFF"` | nothing runs: position and heading unchanged, outcome refused, obstacle (5,7) |
| Bad command character | `"FX"` | raise `ValueError` |
| Invalid grid | odd `width`, non-positive dimension, or start off-grid | raise `ValueError` |

</frozen-after-approval>

## Code Map

Greenfield — `cdfe805` holds only `TASK.md`, `AGENTS.md`, `.gitignore`. Every file below is new.

- `TASK.md` -- authoritative requirement statement; consult for twist wording, do not restate it in comments
- `AGENTS.md` -- states uv + pytest, stdlib only; the `pyproject.toml` below makes its `uv run pytest` line real

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml` -- package metadata, src layout, `requires-python = ">=3.11"`, pytest dev dependency
- [x] `src/rover/geometry.py` -- `Heading` (`left`/`right`/`opposite`), `Position`, `Planet.step()` (wrap + pole crossing) and `Planet.has_obstacle()` -- isolates twist-1 arithmetic for testing without a rover
- [x] `src/rover/rover.py` -- `Rover.execute()`, `position`, `heading`, `discovered_obstacles`; `Outcome` and `Report` -- twist 2: pre-flight simulation against known obstacles, then real execution
- [x] `src/rover/__init__.py` -- export the public names
- [x] `tests/test_geometry.py` -- wrapping, both pole crossings, backward crossings, round-trip reversibility, validation errors
- [x] `tests/test_movement.py` -- turning, multi-command strings, case handling, bad characters
- [x] `tests/test_obstacles.py` -- bump stops the rover, abandons the rest, leaves position and heading intact
- [x] `tests/test_learning.py` -- discovery order, no duplicates, refusal against known obstacles, turn-only strings refused as a whole

**Acceptance Criteria:**
- Given a rover on the north pole row facing north, when it executes `"F"`, then it is on the same row at the antipodal longitude facing south.
- Given a rover that has bumped an obstacle, when asked for discovered obstacles, then it appears exactly once however many times it was hit.
- Given a string whose simulated path hits a discovered obstacle, when it executes, then no command runs and the report names that obstacle.
- Given a string whose path hits an undiscovered obstacle, when it executes, then commands before the bump take effect, the rest are abandoned, and the obstacle is recorded.

## Implementation Notes

- `Planet.step()` resolves a backward move by flipping the direction first (`heading.opposite()`), then applies one crossing rule for both directions: leaving a pole row keeps `y`, shifts `x` by `width // 2`, and returns `heading.opposite()`. So `FB` is a no-op at a pole without a special case.
- A blocked move returns the rover's *current* position and heading, so a bump that would have crossed a pole cancels the heading flip too (`tests/test_obstacles.py::test_a_blocked_move_leaves_the_heading_alone_at_a_pole`).
- `execute()` parses and validates the whole string before anything runs, so `"FX"` raises `ValueError` without moving the rover.
- Matrix row "no duplicate learning" is unreachable as literally written: once an obstacle is known the pre-flight refuses the string, so a second real bump cannot occur. The dedup guard in `_learn` is defence in depth; the covering test drives at the obstacle again and asserts a single entry, and the refusal is what it observes. Consistent with the Design Notes ("the real run cannot hit a known obstacle").
- Beyond the spec: obstacles declared off-grid raise `ValueError` (an unreachable obstacle is dead data), and `Rover` accepts a heading letter as well as the enum. Both are additive; neither changes a specified behavior.
- Verified: `uv run pytest` -> 62 passed, no skips or deselects; `uv run python -c "import rover"` resolves to `src/rover/__init__.py`.

- Review round (12 patches): `_parse` now judges each character of the original string on its own, so a ligature cannot expand into two commands and the error names the character as typed with its index; `Report.stopped` documents the REFUSED case; `Iterable` comes from `collections.abc`; and `Planet` gained an explicit `__init__` so its `obstacles` field can be honestly typed `frozenset[Position]` while still accepting any iterable of pairs. Frozen-dataclass behaviour verified intact afterwards: `FrozenInstanceError` on assignment, working `__eq__`/`__hash__`/`__repr__`.
- Suite grew 62 -> 73. Five previously unpinned rules now fail under mutation, each re-verified independently in this session: removing the `_learn` guard, narrowing `stopped` to BLOCKED, dropping the frozenset write-back, ignoring `x` in `contains`, and dropping `.strip()` in `Heading.parse` each break at least one test.
- Refusal semantics were left untouched under review pressure; see Review Triage Log row 1.

## Spec Change Log

## Review Triage Log

Three layers ran: blind-hunter (24 findings), edge-case-hunter (11), verification-gap (5 plus notes). Every claim below was checked against the code, and every mutation claim re-run independently before its verdict.

| # | Finding (source) | Verdict | Evidence |
|---|---|---|---|
| 1 | Pre-flight walks through unknown obstacles, so a string is refused naming a known obstacle beyond a nearer unknown one; the near one is never learned (all three layers) | false | Reproduced exactly: unknown (5,6), known (5,7), `execute("FF")` -> REFUSED naming (5,7), nothing moves. This is what TASK.md specifies: refusal triggers on what the rover "can tell in advance ... about an obstacle it already knows about", and mandates "the rover does not move at all". The proposed fix -- drive until the real bump -- would violate that clause. Behaviour is correct; the code is not changed. |
| 2 | The "does not record it twice" rule is pinned by no running test; the `_learn` guard is unreachable (verification-gap, blind-hunter) | medium | Confirmed by mutation: unconditional append leaves 62/62 green. The guard is unreachable because the pre-flight refuses first -- so the rule needs pinning where it lives. -> patch |
| 3 | `Report.stopped` never asserted for REFUSED (verification-gap, blind-hunter) | medium | Confirmed by mutation: narrowing to `is Outcome.BLOCKED` leaves 62/62 green. A caller branching on `stopped` would treat a refused string as a clean run. Docstring also misdescribes REFUSED. -> patch |
| 4 | `_parse` uppercases the whole string before validating (blind-hunter, edge-case-hunter) | low | Both symptoms reproduced: `execute("\ufb00")` runs two forward moves and completes; `execute("fx")` reports `'X'`, never typed by the caller. One defect, two symptoms. -> patch |
| 5 | Frozenset normalisation untested; a generator-built planet would silently lose its obstacles (verification-gap) | low | Confirmed by mutation: dropping the write-back leaves 62/62 green. Current code is correct -- generators work today -- but nothing detects a regression. -> patch |
| 6 | Off-grid obstacle rejection only tested for y (verification-gap) | low | Confirmed by mutation: weakening the check to y-only leaves 62/62 green, accepting a phantom obstacle at x=12 on a 10-wide grid. -> patch |
| 7 | `Heading.parse`'s `.strip()` is unobserved (verification-gap) | low | Confirmed by mutation: removing `.strip()` leaves 62/62 green while `" n "` starts raising. -> patch |
| 8 | `test_a_pole_round_trip_is_a_no_op` SOUTH parameter never touches a pole (blind-hunter) | low | Verified: at (2,5) on 10x6 facing S, F goes to (2,4) -- an ordinary round trip. Half the test's stated coverage is absent. -> patch |
| 9 | `test_commands_are_case_insensitive` compares two rovers, not expected values (blind-hunter) | low | True: the assertion passes if both paths are wrong identically. -> patch |
| 10 | Inaccurate test comments: `"RF"` reaches (4,5) not (3,5); `bump()` docstring overclaims generality (blind-hunter) | low | Verified by tracing both. -> patch |
| 11 | Missing cheap geometry cases: width=2, repeated crossings in one string, duplicate obstacles (blind-hunter) | low | True gaps, all trivial to add. -> patch |
| 12 | `typing.Iterable` deprecated alias; redundant quoted forward refs; `Planet.obstacles` annotated as one type and stored as another (blind-hunter) | low | True: the field declares `Iterable[tuple[int,int]]` and holds `frozenset[Position]`, so readers get the wrong static type. -> patch |
| 13 | Rover may start on an obstacle (blind-hunter, edge-case-hunter) | low | Real but unspecified by TASK.md, and the fix adds a guard for state never demonstrated to cause harm. Rejected under the low-finding rule. |
| 14 | `Planet.step`/`has_obstacle` accept off-grid positions (blind-hunter, edge-case-hunter) | low | Unreachable through `Rover`, which validates at construction and only ever passes squares `step` returned. Fix adds guards. Rejected. |
| 15 | `Planet.step` with a raw string heading silently moves south and returns the string (edge-case-hunter) | low | Reproduced: `step(Position(5,5), "N")` -> `(Position(5,4), 'N')`. Unreachable via `Rover` (headings are parsed at construction); fix adds a branch. Rejected, noted here because it is a genuine trap for direct callers. |
| 16 | Wrong-arity position, non-str commands, malformed obstacle tuples, non-integral coordinates all raise TypeError/AttributeError rather than ValueError (edge-case-hunter x4, blind-hunter) | low | All true; all require passing malformed input no demonstrated caller passes. Fixes add type guards. Rejected. |
| 17 | Traversal loop duplicated between `execute` and `_simulate` (blind-hunter) | low | Real duplication, and a genuine divergence risk if movement semantics change. But the fix is a refactor introducing an abstraction over two loops that differ in kind (one mutates and learns, one is pure), and both are covered. Rejected as not worth the churn. |
| 18 | No domain exception hierarchy; `Raises:` undocumented; no progress index on `Report`; no `knows()`/seed/clear learning API (blind-hunter x4) | low | All add public surface beyond what TASK.md asks for. Rejected. |
| 19 | No README, no py.typed, no linter/formatter/CI, no conftest.py, pyproject missing readme/license/classifiers/scripts (blind-hunter x5) | low | None named a harm to a user or developer of this repo: TASK.md is the explanatory document, module docstrings carry the geometry, and there is no downstream consumer. Rejected. |
| 20 | Missing `.gitignore` (blind-hunter) | false | It exists at the repo root, committed in cdfe805 with `.venv/`, `__pycache__/`, `.pytest_cache/`. The reviewer saw only the diff, which excludes pre-existing files. |
| 21 | Bare `pytest` fails and this is documented nowhere (blind-hunter) | false | `AGENTS.md` states `uv run pytest` under Running and verifying. Reviewer saw only the diff. Its stale "no pyproject.toml yet" wording is real -- see defer below. `--strict-markers`/`--strict-config` rejected as low. |
| 22 | Spec AC "commands before the bump take effect" is contradicted when a known obstacle sits beyond an unknown one (edge-case-hunter) | low | The AC is under-qualified for the overlap case; the code follows TASK.md. Rejected: its only fix is to edit this build's spec. |
| 23 | Task list says test_learning covers "turn-only strings refused as a whole" but the test asserts COMPLETED (edge-case-hunter) | low | The code is right -- TASK.md says "Turning is fine either way", and `test_refusal_swallows_the_turns_too` covers the intended meaning (turns do not survive a refusal). The task bullet is loosely worded; its only fix is to edit this build's spec. Rejected. |

**Deferred:** `AGENTS.md` still reads "TODO, no `pyproject.toml` exists yet" under Running and verifying. Now stale, but the fix edits an agent-context file, so it routes to deferred work rather than this build.


## Design Notes

**Why a pole crossing reverses the heading, backward moves included.** `TASK.md` fixes the forward case and says a backward move crosses "the same way a forward move in the opposite heading would" — which fixes the landing square but not the resulting heading. Reversal is the reading that keeps `B` the inverse of `F`:

```
(2,5) facing N, height 6  --F-->  (7,5) facing S    # stated by TASK.md
(7,5) facing S            --B-->  (2,5) facing N    # reversal: back where it started
                                  (2,5) facing S    # non-reversal: FB loses the heading
```

The body never turns; what flips is which map direction "forward" points to on the far side. So: any pole crossing reverses N<->S, and `FB` is always a no-op.

**Refusal is total.** "Refused as a whole" means no command runs, turns included — `"RLFF"` refused leaves the heading untouched. "Turning is fine either way" means a turn can never itself bump or trigger a refusal, not that turns survive a refusal.

**Pre-flight simulation.** `execute()` replays the string against known obstacles only; if that hits one, refuse. Otherwise run for real, where unknown obstacles can still stop it. The real run cannot hit a known obstacle — it follows the simulated path up to the first unknown bump.

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass, no collection errors
- `uv run python -c "import rover; print(rover.Rover)"` -- expected: imports from the installed src layout, no path hacks

## Suggested Review Order

**Twist 1 — the poles are real**

- Start here: one crossing rule serves forward and backward, so `FB` is always a no-op.
  [`geometry.py:113`](../../src/rover/geometry.py#L113)

- Backward resolves to the opposite direction first; everything downstream is shared.
  [`geometry.py:94`](../../src/rover/geometry.py#L94)

- The heading reversal that makes a pole crossing reversible.
  [`geometry.py:46`](../../src/rover/geometry.py#L46)

**Twist 2 — the rover learns**

- The whole of twist 2: look ahead on known obstacles, then drive for real.
  [`rover.py:88`](../../src/rover/rover.py#L88)

- Pure replay over known obstacles only — it never reads the planet's true set.
  [`rover.py:123`](../../src/rover/rover.py#L123)

- A bump leaves position and heading untouched, then records the obstacle.
  [`rover.py:97`](../../src/rover/rover.py#L97)

- Discovery order, recorded once; unreachable twice, guarded anyway.
  [`rover.py:143`](../../src/rover/rover.py#L143)

**Public surface**

- Validates per character on the original string, so a ligature cannot become two commands.
  [`rover.py:108`](../../src/rover/rover.py#L108)

- Explicit `__init__` lets the frozen field be typed as what it actually holds.
  [`geometry.py:65`](../../src/rover/geometry.py#L65)

- Three outcomes, so callers can tell a bump from a refusal.
  [`rover.py:11`](../../src/rover/rover.py#L11)

**Tests worth reading**

- The sharpest case: look-ahead follows the rover across a pole, then refuses the same route.
  [`test_learning.py:135`](../../tests/test_learning.py#L135)

- A blocked crossing cancels the heading flip too.
  [`test_obstacles.py:31`](../../tests/test_obstacles.py#L31)

- Round trip parametrised over both pole rows, asserting the midpoint.
  [`test_movement.py:99`](../../tests/test_movement.py#L99)

- Pins the dedup rule where it lives, since no command sequence can re-bump.
  [`test_learning.py:43`](../../tests/test_learning.py#L43)
