---
title: 'Mars rover with real poles and a learning obstacle map'
type: 'feature'
created: '2026-09-01'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '20b692674a96c7b0b8ed6ebf0120f88bf9382a93'
context: ['{project-root}/TASK.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository has no code. `TASK.md` asks for a Mars rover kata with two twists: the grid maps a sphere whose pole rows are crossed rather than wrapped, and the rover starts with no obstacle map and learns obstacles by bumping into them.

**Approach:** A single Python package `mars_rover` (stdlib only, pytest for tests, `uv` for the environment) with a geometry-only `Planet`, a `Rover` that executes command strings, and a `Report` value describing the outcome. Every rule in `TASK.md` gets a test.

## Boundaries & Constraints

**Always:**
- `x` is longitude, wraps modulo `width`. `y` is latitude, row 0 is the south pole row, row `height - 1` the north pole row. Never wrap `y`.
- Crossing a pole: the rover stays on the same pole row, `x` becomes `(x + width // 2) % width`, and heading flips 180 degrees. This applies to backward moves too, so heading always flips on a crossing.
- Turning never hits anything and is never refused.
- Prediction uses only the rover's discovered obstacles. A command string whose simulated path bumps a known obstacle is refused whole: no state change, report names that obstacle.
- Otherwise execute against the planet. On bumping an unknown obstacle: rover keeps the position and heading reached so far, records the obstacle once, abandons the rest, report names it.
- Validate the whole command string before executing; an unknown letter raises `ValueError` and nothing moves.
- `Planet` rejects odd `width` and non-positive dimensions with `ValueError`.

**Never:**
- No third-party runtime dependencies. No CLI, no I/O, no persistence.
- Never let the rover read `Planet.obstacles` for prediction; only for the actual move check.

## I/O & Edge-Case Matrix

Planet 4x3 unless stated; rover starts at (0, 0) heading N.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Basic moves | `FFRFF` | (2, 2) heading E, completed | N/A |
| Backward | `B` from (0, 1) N | (0, 0) N | N/A |
| Longitude wrap | `RB` at (0, 0) | (3, 0) E | N/A |
| North pole cross | `F` from (0, 2) N | (2, 2) heading S | N/A |
| South pole cross | `F` from (1, 0) S | (3, 0) heading N | N/A |
| Backward over pole | `B` from (0, 2) heading S | (2, 2) heading N | N/A |
| Unknown obstacle | obstacle (0, 2); `FFRF` | stops at (0, 1) N, blocked by (0, 2), rest abandoned; discovered = [(0, 2)] | N/A |
| Known obstacle refused | discovered (0, 2); at (0, 0) N; `FF` | no move, refused naming (0, 2) | N/A |
| Refusal after a turn | discovered (0, 2); at (0, 1) E; `LF` | no move, heading stays E, refused | N/A |
| Turn-only near known | discovered (0, 2); at (0, 1) N; `LR` | completed, heading N | N/A |
| Repeated bump | bump (0, 2) twice via separate strings | discovered list has one entry | N/A |
| Obstacle across pole | obstacle (2, 2); `F` from (0, 2) N | no move, heading stays N, blocked by (2, 2) | N/A |
| Discovery order | bump A then B | discovered == [A, B] | N/A |
| Bad command | `FX` | nothing moves | `ValueError` |
| Odd width | `Planet(5, 3)` | rejected | `ValueError` |

</frozen-after-approval>

## Code Map

Greenfield: no existing code. `AGENTS.md` says run tests with `uv run pytest` and that latitude never wraps.

- `pyproject.toml` -- new; package metadata, `requires-python`, pytest in the `dev` dependency group so `uv run pytest` works.
- `mars_rover/__init__.py` -- new; re-exports `Planet`, `Rover`, `Heading`, `Report`, `Outcome`.
- `mars_rover/planet.py` -- new; `Heading` enum with `turn_left`, `turn_right`, `opposite`; `Planet(width, height, obstacles)` with `step(position, heading) -> (position, heading)` doing wrap and pole crossing. No obstacle logic here beyond storing the set.
- `mars_rover/rover.py` -- new; `Outcome` enum (COMPLETED, BLOCKED, REFUSED), `Report` frozen dataclass (position, heading, outcome, obstacle), `Rover(planet, position, heading)` with `execute(commands) -> Report`, `position`, `heading`, `discovered_obstacles`. One private simulate function used for both prediction and execution, parameterized by the obstacle set it checks against.
- `tests/test_planet.py`, `tests/test_rover.py` -- new; one test per matrix row plus discovery-order and idempotent-recording cases.

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml` -- create with project name `mars-rover`, `requires-python = ">=3.12"`, `[dependency-groups] dev = ["pytest"]`, pytest `testpaths = ["tests"]` -- makes `uv run pytest` the working invocation.
- [x] `mars_rover/planet.py` -- implement `Heading` and `Planet.step` -- geometry in one place, unit-testable without a rover.
- [x] `mars_rover/rover.py` -- implement `Outcome`, `Report`, `Rover.execute` with predict-then-execute -- Twist 2 rests on the simulate function being shared.
- [x] `mars_rover/__init__.py` -- export public names.
- [x] `tests/test_planet.py` -- wrap, both pole crossings, backward crossing, validation.
- [x] `tests/test_rover.py` -- every remaining matrix row, discovery order, no duplicate recording, refused string leaves state untouched.
- [x] `AGENTS.md` -- remove the TODO on the test invocation line once `uv run pytest` is verified against the new `pyproject.toml`.

**Acceptance Criteria:**
- Given any command string, when it completes, is blocked, or is refused, then `Report.position` and `Report.heading` equal the rover's own `position` and `heading` afterwards.
- Given a refused string, when the rover is inspected, then position, heading, and discovered obstacles are unchanged.
- Given a fresh checkout, when `uv run pytest` runs, then all tests pass with no third-party imports besides pytest.

## Implementation Notes

- Implemented by subagent; committed on `main` as `feat(rover): implement mars rover with real poles and learned obstacles`.
- Backward moves step in the opposite heading and un-flip afterwards, so heading flips only on a pole crossing.
- `pyproject.toml` sets `pythonpath = ["."]` so the package imports without a build step. `uv.lock` committed; `.gitignore` gained `.venv/`, `__pycache__/`, `.pytest_cache/`.
- Tests seed already-known obstacles via the private `_discovered` list; no public preload API in the spec.
- Verified: `uv run pytest` 35 passed on Python 3.12.12; only pytest and its deps installed beyond stdlib.

## Spec Change Log

## Review Triage Log

| # | Layer | Finding | Verdict | Evidence / route |
|---|-------|---------|---------|------------------|
| 1 | edge | Obstacles off grid accepted, never hit | medium | Probed: `Planet(4,3,obstacles=[(9,9)])` then `FF` completes. Typo silently vanishes. Route: patch (group A) |
| 2 | edge | `step` with off-grid `y` treated as pole crossing | medium | Only reachable via unvalidated start position; same root as 1. Route: patch (group A) |
| 3 | edge | Rover start off grid or on an obstacle accepted | medium | Probed: start `(7,5)` on 4x3 reports `(1,5)` heading S. Route: patch (group A) |
| 4 | edge | `commands` not a `str` | low | Iterating `None` already raises `TypeError` loudly; guard adds a branch for a case no caller reaches. Rejected |
| 5 | vgap | BLOCKED heading never asserted after a turn or on `B` | medium | Pre-verified by mutants A and B surviving 35 tests. Route: patch (group B) |
| 6 | vgap | `not in self._discovered` guard unreachable | false | Reviewer states it is not a defect; harmless defensive check, no bad outcome. Rejected |
| 7 | vgap/blind | Tests seed knowledge via private `_discovered` | low | A rename fails the fixture loudly; fix adds public surface or rewrites fixtures. Rejected |
| 8 | blind | Start position unvalidated | medium | Duplicate of 3. Route: patch (group A) |
| 9 | blind | Start on an obstacle accepted | medium | Duplicate of 3. Route: patch (group A) |
| 10 | blind | Obstacle coordinates unvalidated | medium | Duplicate of 1. Route: patch (group A) |
| 11 | blind | `Planet.step` trusts input | medium | Duplicate of 2. Route: patch (group A) |
| 12 | blind | `obstacles` parameter untyped | low | True; one annotation. Route: patch (group C) |
| 13 | blind | `Position` used in public signatures but not exported | low | True; one export line. Route: patch (group C) |
| 14 | blind | `Report.obstacle` meaning per outcome undocumented | low | True; one docstring. Route: patch (group C) |
| 15 | blind | Duplicate test `test_backward_crossing_is_forward_in_opposite_heading` | low | `Heading.S.opposite is Heading.N`, identical to `test_north_pole_crossing`. Route: patch (group B, delete) |
| 16 | blind | `test_latitude_never_wraps` redundant | false | It pins the convention named in `AGENTS.md`; redundancy is not a bad outcome. Rejected |
| 17 | blind | Backward-over-pole heading rule unexplained in code | low | True; one comment in `_simulate`. Route: patch (group C) |
| 18 | blind | Missing test: blocked after turn / after pole crossing | medium | Same gap as 5; probed both behave correctly. Route: patch (group B) |
| 19 | blind | Missing test: `B` blocked and refused | medium | Same gap as 5. Route: patch (group B) |
| 20 | blind | Missing test: known obstacle across a pole refused | medium | Prediction path across pole untested. Route: patch (group B) |
| 21 | blind | Lowercase / whitespace command policy undecided | false | Spec: unknown letter raises `ValueError`; `f` is an unknown letter. Decided and tested |
| 22 | blind | Two simulation passes instead of one | false | Spec Design Notes require full-string prediction; a single pass would block at an unknown obstacle before seeing a known one |
| 23 | blind | `_Simulation` near-duplicates `Report` | low | Developer-only, refactor not a direct correction. Rejected |
| 24 | blind | No `[build-system]`, relies on `pythonpath` | low | No consumer imports from another directory; spec asks for a single package with tests. Rejected |
| 25 | blind | `requires-python >=3.12` stricter than needed | false | Spec task sets 3.12; user said whatever is installed, and 3.12 is what `uv` resolves |
| 26 | blind | `uv.lock` absent from diff | false | Excluded from the review diff deliberately; `uv lock --check` passes |
| 27 | blind | `_bmad-output/` neither tracked nor ignored | maybe-false | Repo hygiene decision for the user; fix edits `.gitignore` policy outside intent. Route: defer |
| 28 | blind | `AGENTS.md` provenance line stale after hand edit | low | Fix edits an agent-context file. Route: defer |
| 29 | blind | Linear `index()` in heading turns | false | Four-element tuple; no measurable outcome. Rejected |
| 30 | blind | `Planet` lacks `__repr__`/`__eq__` | low | Cosmetic in failure output; more than a direct correction. Rejected |
| 31 | blind | No README or usage example | low | Not requested by `TASK.md`; `__init__` docstring and spec example exist. Rejected |

## Design Notes

- Prediction simulates the full string against the discovered set, so `FF` with an unknown obstacle at step 1 and a known one at step 2 is refused. That is what "can tell in advance" means from the rover's knowledge; the unknown obstacle stays undiscovered.
- A move onto an obstacle across a pole blocks the whole step, including the heading flip, because "the rover does not move".

```python
planet = Planet(4, 3, obstacles={(0, 2)})
rover = Rover(planet, (0, 0), Heading.N)
rover.execute("FF")   # Report((0, 1), N, BLOCKED, (0, 2))
rover.execute("F")    # Report((0, 1), N, REFUSED, (0, 2))
rover.discovered_obstacles  # ((0, 2),)
```

## Verification

**Commands:**
- `uv run pytest` -- expected: all tests pass.
- `uv run python -c "import mars_rover"` -- expected: no import errors, no third-party modules.

## Suggested Review Order

**Predict-then-execute (Twist 2)**

- Entry point: validate, predict against known obstacles, then execute against the planet.
  [`rover.py:65`](../../mars_rover/rover.py#L65)

- Prediction reads only the discovered list; a hit refuses the whole string.
  [`rover.py:71`](../../mars_rover/rover.py#L71)

- One shared simulation; the obstacle set passed in is the only difference.
  [`rover.py:85`](../../mars_rover/rover.py#L85)

- Backward moves un-flip afterwards so heading changes only on a pole crossing.
  [`rover.py:100`](../../mars_rover/rover.py#L100)

**Sphere geometry (Twist 1)**

- Off a pole row: same row, longitude shifted by half the width, heading flipped.
  [`planet.py:76`](../../mars_rover/planet.py#L76)

- Step is pure geometry; obstacle checks live in the rover.
  [`planet.py:65`](../../mars_rover/planet.py#L65)

**Input validation (added in review)**

- Off-grid obstacles rejected, since they could never be hit.
  [`planet.py:59`](../../mars_rover/planet.py#L59)

- Start position must be on the grid and not on an obstacle.
  [`rover.py:43`](../../mars_rover/rover.py#L43)

**Reporting surface**

- `Report.obstacle` meaning per outcome; state unchanged on REFUSED.
  [`rover.py:21`](../../mars_rover/rover.py#L21)

**Tests and config**

- Fixture seeds known obstacles through the private list; see triage row 7.
  [`test_rover.py:6`](../../tests/test_rover.py#L6)

- The judgment call: unknown at step 1, known at step 2, string refused.
  [`test_rover.py:147`](../../tests/test_rover.py#L147)

- Known obstacle on the far side of a pole is refused by prediction.
  [`test_rover.py:131`](../../tests/test_rover.py#L131)

- Backward over the pole ends heading N.
  [`test_rover.py:46`](../../tests/test_rover.py#L46)

- `pythonpath` makes `uv run pytest` work without a build step.
  [`pyproject.toml:12`](../../pyproject.toml#L12)
