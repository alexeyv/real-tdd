# Ping-pong run, Mars Rover, 2026-09-01

Two Claude Code sessions (Fable 5.1 for the first two turns, then Opus 5
at high effort) ran `skills/real-tdd` against `task.md`. Ping wrote the
test list and the first red; the baton alternated on every red.

| | |
|---|---|
| Turns | 25 |
| Commits | 28 |
| Tests | 44, of which 24 were steps and 20 were written at the end as a regression block for list items already satisfied |
| Test list | 44 items, all checked |
| Production code | 71 lines, `mars_rover.py` |
| Wall time | about 100 minutes, roughly 3.5 minutes per turn |

Files: `task.md` (the human's statement), `test-list.md` (final state),
`journal.md` (one entry per turn, the experiment's data), `mars_rover.py`
and `test_rover.py` (final), `git-log.txt`.

Human interventions: one, after turn 2, a housekeeping note that green
commits must include the test file. Everything else ran unattended.

Findings are summarised in the repository `TODO.md` under "Fix the
problems the run exposed". The control run with a single bmad-build
session on the same task is in `../control/`.
