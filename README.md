# real-tdd

Kent Beck's test-driven development, as he wrote it, run as ping-pong
pairing between two isolated Claude Code sessions.

This is an experiment. It is not a recommendation, and it is not a joke.

## The question

TDD was a design technique. The claim was that writing one failing test at
a time, before you know how you will pass it, and then removing the
duplication the cheapest passing code created, produces a better interface
and implementation than deciding the design up front. The tests were a
by-product.

Skills that put "TDD" in front of a language model generally keep the
red-green-refactor vocabulary and remove the condition that made it work:
the test's author did not yet know the implementation. In a single model
context the test and the code come out of the same pass, so the test
cannot push back on anything.

Across two contexts it can. So: two sessions, one working tree, ping-pong
rules. One writes a failing test. The other makes it pass, refactors,
commits, and writes the next failing test. Repeat until the test list is
empty. Neither session sees the other's reasoning, only the files.

The experiment asks whether the tests drive anything under those
conditions. Specifically:

1. Does the interface that emerges differ from what a single session
   writes from the same task statement in one pass?
2. Does the test list change during the run? Beck's list is supposed to
   grow as the code teaches you things. If it never changes, nothing was
   learned from the sequence.
3. Do the sessions actually vary their step size, or do they choose
   Obvious Implementation every time?
4. What does it cost, in turns and tokens, relative to the control?

The journal each run produces is the data.

## Running it

Install the skill by copying or symlinking `skills/real-tdd/` into your
project's `.claude/skills/` (or `~/.claude/skills/` for all projects).
Then, from the repository you want to work in, open two terminals:

```
# terminal 1
claude
> /real-tdd ping Implement a Money class that supports addition across currencies with a rate table

# terminal 2
claude
> /real-tdd pong
```

Start `ping` first. It writes the task and the test list, writes the first
failing test, and hands over. From then on the sessions alternate on their
own; the baton is a file in `.real-tdd/`, and each session polls it.

Everything the run produces is in the working tree: the code, the tests,
one commit per green, and `.real-tdd/journal.md`.

When a session finds the task ambiguous it writes `human` to the baton and
a question in the journal, and both sessions wait. Answer by appending to
`.real-tdd/task.md`, then write the asking session's role (`ping` or
`pong`) to `.real-tdd/baton`.

## Running the control

Same task statement, one session, no skill, the instruction "implement
this with whatever tests you think it needs". Compare against the
ping-pong run:

- the public interface (signatures, types, names);
- the final test list against the tests that exist;
- the journal's Surprise lines, which are the only direct evidence that a
  test taught somebody something;
- cost.

A blind reviewer who sees both results and neither process is the right
judge of the first item.

## What is in here

- `skills/real-tdd/SKILL.md`: routes each session to its role.
- `skills/real-tdd/references/ping.md`, `pong.md`: the two role prompts.
- `skills/real-tdd/references/turn.md`: the loop both roles run.
- `skills/real-tdd/references/glossary.md`: the terms the protocol uses,
  one meaning for both sessions.
- `WHAT_IS_REAL_TDD.md`: what Beck wrote, with sources, so the skill can
  be checked against the technique it claims to run.
- `tools/session_tokens.py`: sums token usage from the Claude Code session
  logs of a run.
- `runs/`: one directory per run, with the ping-pong artifacts, the
  control, and a comparison.

## Status

Three runs of the same Mars Rover task, all in `runs/`. The first has a
bmad-build control and used the skill text at tag `run-1`. The second and
third ran on successive revisions of the skill and carry the exact text
they used in `skill-as-run/`. Each run directory has a README with the
numbers, the token usage, and what the run showed.

## License

MIT.
