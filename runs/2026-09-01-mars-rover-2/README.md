# Mars Rover, second ping-pong run

Same task statement as `../2026-09-01-mars-rover/`, run with the revised
skill: role prompts split into `ping.md`, `pong.md`, and a shared
`turn.md`; glossary; the mitigations for the first run's failure modes.
The exact skill text the sessions read is in `skill-as-run/`. The `human`
baton was added to the skill during this run and was not in effect.

Both sessions ran Claude Code on Opus 5 with effort high. Prompts, in
full: `/real-tdd ping` and `/real-tdd pong`, with the task pre-written to
`.real-tdd/task.md`. No other prompt was sent to either session.

## Numbers

| | Run 1 | Run 2 |
|---|---|---|
| Wall time, first to last commit | ~100 min | 34 min |
| Turns | 25 | 27 |
| Commits | 28 | 32 |
| Tests | 44 | 39 |
| Tests that passed on arrival (regression) | 20 | 12 |
| Production lines | 71 | 51 |
| Human interventions | 1 | 0 |
| Green by Fake It / Obvious / Triangulate | | 2 / 21 / 3 |

## What the mitigations did

- **Test file in the commit.** Pong's first green folded the untracked
  test file in and said so. No commit in the run lacks its test.
- **Timestamps from the clock.** Every entry carries `date -u` output and
  they are monotonic across both sessions.
- **List checked against the task.** The list was faithful. Nothing on it
  contradicted the task at any point, and the clause that split run 1
  (unknown rock nearer than a known one) never became an item; the
  refusal was implemented from the rover's own map, which is the task's
  reading and the control's.
- **"Also satisfied" line.** Used honestly and mostly read as "none". When
  a green did cover another item (west wrap by modulo, right turns by
  inverting the left table), the session said so and then declined to
  check the item off without a test. Twelve tests still passed on arrival,
  including all of the last five. The line made the overshoot visible; it
  did not prevent it.
- **"Interface decided" line.** Filled in six times: module and class,
  `execute`, `obstacles=` on the constructor, `blocked_by`, `blocked_by is
  None`, `discovered`. Every interface fact in the code traces to one
  entry.
- **Passing new test rule.** Followed to the letter, including two commits
  in one turn to pin a free behavior separately from the green.

## What the run surfaced that the skill did not cover

- **Two ambiguities in the task, both resolved inside a test.** Turn 22:
  whether a backward pole crossing gives the same end state as the
  forward one or applies the same mechanism. Turn 24: once known-obstacle
  refusal exists, the same rock can never be bumped twice, so "not
  recorded twice" has no reachable input. Both sessions noticed, wrote it
  up, and picked a reading, because the protocol offered no other move.
  This is why the `human` baton was added.
- **The end of the run had no red.** After the refactor that unified
  bumping and refusal into one walk against two collections, five task
  sentences became consequences of one function, and the last five tests
  could not fail. Ping's closing entry calls this the strongest argument
  for refactoring in the run and the most uncomfortable.
- **Left for the human.** The rover holds the world's obstacle list next
  to its own map. Pong declined to invent a `Planet` at turn 13 and no
  test ever forced one. Ping's final entry asks whether that is the
  method being honest about what the tests demanded or the method missing
  what a designer would see on day one.

## Tokens

Same method as run 1 (`tools/session_tokens.py`).

| Session | Output | API calls | Cache writes | Cache reads |
| --- | ---: | ---: | ---: | ---: |
| ping | 80,030 | 111 | 136,563 | 10,528,138 |
| pong | 56,169 | 112 | 134,858 | 9,204,544 |
| **total** | 136,199 | 223 | 271,421 | 19,732,682 |
| run 1 ping-pong | 92,639 | 165 | 311,695 | 11,542,804 |
| run 1 control | 93,266 | 137 | 593,707 | 11,054,047 |

Run 2 cost half again as much as run 1: more turns, more calls per turn,
and a context that grew with the journal and was re-read on every call. Ping, which starts the run and writes the
list, reads and writes more than pong in both runs. Against the control,
ping-pong on the revised skill reads 1.8 times the cache and produces 1.5
times the output for a fifth of the production code.

## Reading

A third of the wall time of run 1 for a comparable result, with no
intervention, and half again the tokens. The journals do not say where
run 1's extra hour went; the turn count and the work per turn are
similar. Same code shape as run 1: one class, tuples, strings, a compass
table. The design is the one the starter test fixed at turn 1, and the
journal is again about the list and the protocol rather than about the
code wanting a different shape. The kata caveat from the first run's
README applies unchanged.

## Files

Task, final test list, journal, final code and tests, git log,
`repo.bundle` with the complete history (restore with `git clone
repo.bundle`), and `skill-as-run/` with the skill text exactly as
installed for this run.
