<!-- bmad:context -->
<!-- Verified 2026-09-01 against an empty repository (no commits yet). Managed by
     bmad-project-context; edits inside this block are replaced on refresh. Keep
     anything you want preserved outside the markers. -->

## bmad-build-mars-rover

A Mars rover kata with two twists: the grid is a sphere, so moving off a pole row
crosses the pole rather than wrapping, and the rover discovers obstacles by bumping
into them. Python 3 with pytest, managed with uv. `TASK.md` is the spec of record;
BMAD planning artifacts land in `_bmad-output/`.

## Policy

- Never hand-edit `_bmad/config.toml` or `_bmad/config.user.toml` — the installer
  regenerates both on every install. Pinned overrides go in `_bmad/custom/config.toml`.

## Where things are

- The full task, both twists included: `TASK.md`. Interface, module layout, and report
  formats are deliberately left open — decide them, don't hunt for them.

## Running and verifying

- TODO, no `pyproject.toml` exists yet. Once it does: run tests with `uv run pytest`,
  single files while iterating. Bare `pytest` is not installed on this machine and
  would run outside the project environment.
- Add dependencies with `uv add --dev`, never `pip install`.
- Don't add runtime dependencies — the task allows the standard library only, plus
  pytest for tests.

<!-- /bmad:context -->
