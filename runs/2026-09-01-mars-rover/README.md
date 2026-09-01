# Mars Rover, 2026-09-01: ping-pong versus a single bmad-build session

Same task statement (`pingpong/task.md` and `control/TASK.md` differ only
in the closing "Done" paragraph). Both on Opus 5 at high effort, the
ping-pong run after its first two turns.

## Numbers

| | Ping-pong | Control (bmad-build) |
|---|---|---|
| Sessions | 2, alternating | 1, with one implementer subagent and three review subagents |
| Production code | 71 lines, 1 module, 1 class | 267 lines, 2 modules, 6 classes |
| Tests | 44 (24 driven, 20 regression block at the end) | 73 (62 from the implementer, 11 added by review patches) |
| Test files | 1 | 4 |
| Commits | 28 | 1 |
| Wall time | about 100 minutes | about 25 minutes from baseline to final commit, plus 4 minutes of project-context setup |
| Human interventions | 1 (commit hygiene) | 5 (setup answers, AGENTS.md approval, spec approval, two nudges) |

## Interfaces

Ping-pong: `Rover(width, height, x, y, heading, obstacles=())` with
`execute(commands)` returning nothing. State read back through
`position` (a tuple), `heading` (a one-letter string), `stopped_by`
(a tuple or None) and `discovered_obstacles` (a tuple).

Control: `Position` NamedTuple, `Heading` Enum with `left`, `right`,
`opposite`, a `Planet` owning geometry and the true obstacle set, and a
`Rover` whose `execute(commands)` returns a `Report` with an `Outcome`
Enum (completed, blocked, refused). Commands are case-insensitive and
bad characters raise.

## The clause they disagree on

The task says a command string the rover "can tell in advance would bump
into an obstacle it already knows about" is refused whole, and separately
that unknown obstacles are discovered by bumping. When an unknown rock
sits nearer than a known one, the two readings conflict.

- Ping-pong: the test list said the string is not refused and the unknown
  rock is bumped. Implementing that required the rover to consult terrain
  it is not supposed to know. The coder wrote that down in the journal and
  passed the test anyway, because tests are the specification.
- Control: the spec said the string is refused, since the rover's own map
  predicts a known rock. All three review layers flagged that the nearer
  rock is never learned. The controller reproduced it and rejected the
  finding on the task text.

Neither is wrong; the task is ambiguous. What differs is where the
decision was made and by whom: in ping-pong, by whoever wrote the list,
with no check against the task. In the control, in the spec, with the
human asked to approve two other interpretive calls but not this one.

## What the ping-pong journal shows about design pressure

- The Starter Test fixed tuple positions and string headings for the whole
  run before any behavior existed. The control chose an Enum and a
  NamedTuple in the spec.
- Four generalizations satisfied a third of the list before any test
  asked. The sessions noticed the overshoot, adapted (one deliberate
  Fake It against the coder's own confidence), and found the condition
  under which triangulation does not overshoot.
- One refactor was credited to a test: the obstacle check forced splitting
  "where would this land" from "go there". The coder said it would not
  have happened otherwise.
- A new test that passed on arrival exposed a stale-report bug. The rule
  that such a test is not a step made the coder discard it and write the
  test the bug was hiding behind.

## Files

`pingpong/`: task, final test list, journal, final code and tests, git
log. `control/`: task, AGENTS.md, the frozen spec with its review triage
log, deferred work, final code and tests, git log.
