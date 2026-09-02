<!-- bmad:context -->
<!-- Verified 2026-09-01 against the baseline commit (root of main; no prior history). Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## bmad-build-mars-rover-3

Mars rover kata with two twists: a spherical planet with real poles, and a rover that discovers obstacles by bumping into them. Python 3, standard library plus pytest, single package, environments managed with `uv`. The spec is `TASK.md` and is authoritative; planning documents land in `_bmad-output/planning-artifacts/`, implementation notes in `_bmad-output/implementation-artifacts/`.

## Policy

- Commit straight to `main`; no branches or PRs required.

## Running and verifying

- Run tests with `uv run pytest` from the repo root, never bare `pytest`, so they run inside the project environment.

## Conventions that differ from defaults

- Latitude never wraps. The classic kata treats the grid as a torus; here moving off a pole row crosses the pole, flips heading, and shifts longitude by `width / 2`. See `TASK.md`, Twist 1.

<!-- /bmad:context -->
