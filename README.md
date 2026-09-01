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
- `skills/real-tdd/references/glossary.md`: the terms the protocol uses,
  one meaning for both sessions.
- `skills/real-tdd/references/beck.md`: what Beck wrote, with sources, so
  the skill can be checked against the technique it claims to run.
- `runs/`: one directory per run, with the ping-pong artifacts, the
  control, and a comparison.

## Status

One run: `runs/2026-09-01-mars-rover/`. The skill was revised after it to
fix the failure modes that run exposed; the run was made with the earlier
text, which is in git history at tag `run-1`.

## License

MIT.
