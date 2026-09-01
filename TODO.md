# TODO after the Mars Rover run (2026-09-01)

Plan for the next session. Written before compaction so nothing here has
to be re-derived. Run artifacts: `/tmp/real-tdd-mars-rover` (ping-pong,
25 turns, 28 commits, 44 tests, journal in `.real-tdd/journal.md`) and
`/tmp/bmad-build-mars-rover` (control, single session, bmad-build on Opus
high). /tmp does not survive forever: copy both into `runs/` first.

## 1. Copy the runs into the repo

`runs/2026-09-01-mars-rover/pingpong/` gets task.md, test-list.md,
journal.md, final `mars_rover.py`, final `tests/test_rover.py`, and
`git log --format='%h %s'`. `runs/2026-09-01-mars-rover/control/` gets
TASK.md, AGENTS.md, the spec from `_bmad-output/implementation-artifacts/`,
the final source and tests, and the git log. A short README comparing the
two public interfaces and the test counts.

## 2. Fix the problems the run exposed

Each of these was observed, not reasoned about.

- **Green commits left the test file untracked.** Pong's first green
  committed `mars_rover.py` alone; ping's scaffold commit predated the test.
  Two "clean check-ins" with no tests in them and neither session noticed
  until the human said so. Fix: the Refactor step says the commit includes
  the test file; the Receive step says the new test may be the whole file
  if the partner forgot.
- **Journal timestamps were invented.** Ping's stamps ran ten minutes behind
  pong's on interleaved turns. Fix: "take the timestamp from `date -u`".
- **The test list drifted from the task and became binding.** Ping's list
  said a string that would hit an unknown rock before a known one is not
  refused. The task said the rover refuses whatever it can tell in advance
  from its own map, which is the opposite. Nobody checked the list against
  the task; ping implemented the list's version, flagged that it made the
  rover consult terrain it cannot see, and complied because "tests are the
  specification". Fix: the first turn ends with the list checked against
  the task line by line, and the Receive step allows "this test contradicts
  the task" as a handback reason (it is already there; make it concrete).
- **Generalization swallowed a third of the list.** Four generalizations
  (compass cycle, longitude modulo, tuple append, pole clamp) satisfied
  items before any test asked, and the sessions kept picking the items that
  could still fail until only twenty already-green ones were left. Ping
  found the condition under which triangulation does not overshoot: two
  examples at opposite ends of one axis, not two of four table entries.
  Fix: when a generalization is known to satisfy other list items, say
  which ones in the journal at that turn, and check them off as "satisfied
  by <commit>, not driven" rather than leaving them for a regression block
  at the end.
- **Whoever holds the red decides the interface alone.** Tuple positions,
  string headings, obstacles through the constructor: each fixed by one
  session in one test and taken as given by the other. Not a bug in the
  protocol, but the skill should say it plainly so the journal records
  those decisions when they happen.
- **A passing new test found a bug, and the rules handled it.** Pong's
  refusal-report test was green on arrival because a stale field held the
  previous bump. Keep the rule; cite this as the reason it exists.
- **Never exercised:** the three-attempt revert, the empty-list stop before
  the end. Leave them, do not elaborate them.

## 3. Extract the terminology into a shared glossary

`skills/real-tdd/references/glossary.md`: a short definition per term, in
plain English, one paragraph each, no examples longer than a line. Terms
that earn a place because the skill uses them:

Test list, Red, Green, Refactor, Fake It, Obvious Implementation,
Triangulate, One Step Test, Starter Test, Child Test, Assert First,
Evident Data, Isolated Test, Regression Test, Clean Check-in, Do Over,
ping-pong.

These are necessary vocabulary, not jargon; the skill refers to them by
name and both roles need the same meaning. If the skill is ever split into
a ping skill and a pong skill, the glossary stays in one place and the
other skill reads it from there (both are visible to the same session).
`references/beck.md` stays as the source trail.

## 4. Strip the skill text down

Go through `SKILL.md` and take out:

- metaphor and colour: "the working tree is the shared screen, the journal
  is the talking", "keyboard", "seams", "footguns", "landing", anything of
  that kind. Plain English.
- over-prompting: rationale paragraphs that repeat what the glossary now
  says, hedges, second explanations of the same rule.
- anything that instructs the model's judgment where the run showed it did
  not need instruction.

Keep:

- the statement of intent, shortened;
- the protocol skeleton: roles, shared files, the turn in order, the first
  turn, the stop;
- one line per observed failure mode from section 2, as a mitigation;
- the journal format, since it is the data.

Test of done: a reader who knows the glossary can follow the skill with no
sentence read twice, and nothing in it argues.
