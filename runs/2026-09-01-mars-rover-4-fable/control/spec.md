---
title: 'Mars rover with pole crossing and obstacle learning'
type: 'feature'
created: '2026-09-01'
status: 'done'
route: 'in-session'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository has only a task statement (`TASK.md`) and no code. It needs a Python 3 Mars rover implementing the classic kata plus two twists: the grid is a sphere whose poles are crossed rather than wrapped, and the rover starts with no obstacle map, learns obstacles by bumping, and refuses whole command strings that would hit a known obstacle.

**Approach:** One package `mars_rover` with a `Planet` (size plus obstacle set, queried only on an actual move attempt), a `Rover` that executes `F`/`B`/`L`/`R` strings and returns an immutable report, and pytest coverage for every rule in `TASK.md`. Standard library and pytest only, managed with uv. Decisions delegated by the task and made here: the rover is created as `Rover(planet, x, y, heading)`; `execute(commands)` returns a `Report` with position, heading, `blocked_by` (the obstacle hit, or None) and `refused` (True when a known obstacle would be hit, so the rover did not move); `discovered_obstacles()` returns a list of `(x, y)` tuples in discovery order; the known-obstacle pre-check simulates the whole string against the rover's own map only, so an unknown obstacle earlier on the path does not prevent the refusal.

</frozen-after-approval>

## Suggested Review Order

- Entry point: the command loop, dry walk against the rover's own map first, then real moves.
  [rover.py:64](../../mars_rover/rover.py#L64)
- Prediction uses only discovered obstacles, so unknown ones on the path do not prevent refusal.
  [rover.py:94](../../mars_rover/rover.py#L94)
- Pole crossing geometry: same row, half-width shift, face away from the pole; backward travels opposite.
  [planet.py:62](../../mars_rover/planet.py#L62)
- Report shape: `blocked_by` plus `refused` distinguish a bump from a refusal.
  [rover.py:13](../../mars_rover/rover.py#L13)
- Planet validation: even width, in-bounds obstacle pairs, normalised to a frozenset.
  [planet.py:35](../../mars_rover/planet.py#L35)
- Learning tests: discovery order, refusal, prediction through wrap and backward crossing.
  [test_learning.py:1](../../tests/test_learning.py#L1)
- Pole tests, including single-row and two-column planets.
  [test_poles.py:1](../../tests/test_poles.py#L1)
- Classic movement and validation tests.
  [test_classic.py:1](../../tests/test_classic.py#L1)
- Tooling: no build backend, pytest runs from the repo root via `uv run pytest`.
  [pyproject.toml:1](../../pyproject.toml#L1)

## Implementation Notes

- Layout: flat package `mars_rover/` (`planet.py` geometry and obstacles, `rover.py` execution and learning), tests in `tests/`, no build backend (`tool.uv.package = false`, pytest `pythonpath = ["."]`). `uv run pytest` is the verified test command.
- `Planet.step` is pure geometry and returns the landing square plus the heading afterwards; a pole crossing keeps the row, shifts longitude by `width // 2`, and faces the rover away from the pole (opposite of the travel direction). Backward moves travel in the opposite heading, so the resulting heading after a backward crossing is unchanged.
- `Rover.execute` validates the command string (ValueError on anything but F/B/L/R), then runs a dry walk against the rover's own discovered list; a hit refuses the whole string (`Report.refused`, no state change). Otherwise commands run until an obstacle blocks a move, which is recorded once in discovery order.
- Surprise: two of my pole tests assumed a second forward move crosses back. It does not: after crossing the rover faces south, so the next forward move heads for the equator. Tests were corrected; the code matched TASK.md.
- Files: `pyproject.toml`, `mars_rover/__init__.py`, `mars_rover/planet.py`, `mars_rover/rover.py`, `tests/test_classic.py`, `tests/test_poles.py`, `tests/test_learning.py`.

## Review Triage Log

Blind Hunter, 18 findings.

- Rover may start on an obstacle — low, rejected: spec is silent, nothing breaks (the rover simply moves off), and the fix adds a guard for a state no scenario reached.
- `stopped_by_obstacle` true on refusal contradicts its name — low, patched: Report docstring now states a refusal counts and points at `refused` to tell them apart.
- Planet fights the dataclass machinery — low, patched: replaced the hand-written `__init__` with `__post_init__` validation and a single normalisation write.
- 3-element obstacle fails with a confusing unpack error — low, patched: explicit pair check with a clear message, tested.
- Prediction walk duplicates execution walk — low, rejected: real drift risk but covered by tests; a shared send-driven generator is more complexity than a direct correction.
- Untested edge sizes (height 1, width 2, non-positive) — medium (missing coverage), patched: tests added for all three.
- Prediction tests miss backward crossing and longitude wrap — medium (missing coverage), patched: one test walks wrap plus backward crossing onto a known obstacle, with a near-miss control.
- Lowercase/whitespace rejection undocumented — low, patched: `execute` docstring states it; parametrized test covers `ff`, `F F`, newline.
- Invalid-creation test bundles four cases without `match=` — low, patched: split into parametrized tests with message matches.
- `requires-python >= 3.12` stricter than needed — low, rejected: a floor is a choice, no harm shown; older interpreters were not tested so lowering it would be an unverified claim.
- `uv.lock` gitignored — low, deferred: pre-existing from the baseline commit and a project-policy choice for the user.
- AGENTS.md carries a stale TODO on `uv run pytest` — medium, deferred: real (command verified this run) but the fix edits an agent-context file.
- Spec not closed out — false: closing the spec is this workflow's finalize step, which ran after the review.
- Public API uneven (method vs properties, unexported helpers) — low, rejected: `discovered_obstacles()` returns a fresh copy, which a method signals better than a property; exports are a design choice with no harm named.
- No `__repr__` on Rover — low, patched: repr shows position, heading, discovered obstacles; tested.
- No usage example — low, patched: six-line example in the package docstring.
- `Planet.step` takes a boolean flag — low, rejected: readability preference; every call site uses the keyword form.
- "Record once" branch is unreachable — low, patched: kept as an invariant guard with a comment saying why it cannot fire.
