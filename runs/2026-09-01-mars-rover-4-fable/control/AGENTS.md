<!-- bmad:context -->
<!-- Verified 2026-09-01 against an unborn main (no commits yet). Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## bmad-build-mars-rover-2

A Mars rover kata in Python 3: a single package tested with pytest. The full specification is `TASK.md`; read it before touching rover behavior, because it diverges from the classic kata at the poles and in obstacle handling. Planning artifacts go in `_bmad-output/planning-artifacts/`, implementation artifacts in `_bmad-output/implementation-artifacts/`.

## Policy

- No dependencies beyond the standard library and pytest; `TASK.md` requires it.

## Running and verifying

- Run tests with `uv run pytest`, not bare `pytest`, which runs outside the project environment. TODO: verify once `pyproject.toml` exists.

## Conventions that differ from defaults

- Row 0 is the south pole row and row `height - 1` the north; `y` grows northward, `x` eastward.
- Never wrap latitude. A move off a pole row crosses the pole: same row, `x + width/2` modulo `width`, heading reversed. Longitude wraps as usual.
- A command string that would hit a known obstacle is refused whole, before any move. An unknown obstacle stops the rover at the bump and is recorded once, in discovery order.

<!-- /bmad:context -->
