---
name: real-tdd
description: Kent Beck's test-driven development as he wrote it, run as ping-pong pairing between two Claude Code sessions sharing one working tree. Use when the user says /real-tdd, "real TDD", or "ping-pong TDD". Requires a partner session; never simulate the partner.
---

# Real TDD

## Intent

An experiment, not a recommendation. Beck's TDD is a design technique:
write one failing test, make it pass by the cheapest means, remove the
duplication that created, repeat. It depends on the test's author not yet
knowing the implementation. One model context cannot provide that; two can.
So the technique runs across two sessions that share a working tree and
nothing else. The journal is the data, and nothing here assumes what it
will show.

Terms are defined in `references/glossary.md`. Read it first. Sources are
in `references/beck.md`.

## Invocation

```
/real-tdd ping <task statement>     # first session, starts the run
/real-tdd ping                      # first session, task already in .real-tdd/task.md
/real-tdd pong                      # second session, joins the run
```

Both sessions run in the same repository in separate terminals. Start
`ping` first. Your role is the first word of `$ARGUMENTS`; the rest, if
present, is the task statement.

If there is no partner session, stop and say so. Do not play both roles
with a subagent, a fork, or your own reasoning. The run would measure
nothing.

## Shared state

Everything the sessions share is in the working tree and in `.real-tdd/`.
Neither session reads the other's transcript.

| File | Meaning |
|------|---------|
| `.real-tdd/task.md` | The task in the human's words. Written once by `ping`. Not edited after. |
| `.real-tdd/test-list.md` | The test list, as checkboxes. Either session may add items at any time. |
| `.real-tdd/baton` | Whose turn it is: `ping`, `pong`, or `done`. |
| `.real-tdd/journal.md` | One entry per turn, appended by the session that took the turn. |

## The turn

The session named in the baton acts. The other waits.

### Wait

```bash
until [ "$(cat .real-tdd/baton 2>/dev/null)" = "<your role>" ]; do sleep 5; done
```

If the tool times out, run it again. If the baton reads `done`, read the
last journal entry and stop.

### Receive

1. Read the last journal entry, the test list, and `git status`.
2. Run the whole suite. Expect one failing test, uncommitted. The diff is
   your assignment. If the diff is a whole new test file, your partner
   forgot to commit it earlier; it goes into your commit.
3. If the test fails for a reason that is a mistake in the test rather
   than a missing behavior, fix the test only enough to make it fail for
   the right reason, and say so in the journal. Do not change what it
   asserts.
4. If the test asserts something that contradicts `task.md`, say which
   line of the task in the journal and hand the baton back without a green.
5. If the failing test is one you wrote and your partner handed it back,
   skip Green and Refactor. Split it (Child Test), rewrite it, or withdraw
   it and pick another item. Then hand off.

### Green

Make the failing test pass and keep every other test passing, by Fake It,
Obvious Implementation, or Triangulate. Choose by how sure you are. Do not
write code no current test demands; put the need on the list instead.

If your green also satisfies other list items, name them in the journal
and check them off as "satisfied by <commit>, not driven". Do not leave
them to be tested in a block at the end.

After three failed attempts, revert to the last green commit, write in the
journal that the step was too big, and hand the baton back with the test
still red.

### Refactor

Only on green. Remove duplication, including between the test's expected
value and the code. Improve names. Add no behavior. Run the whole suite
after each change.

Commit when green and clean. The commit includes the test file. Use a
conventional-commit subject.

### Red

Write the next failing test. Whoever writes the test decides the interface
it calls; there is no other place that decision gets made, so record it
in the journal when you make one.

1. Pick one item from the list (One Step Test; Starter Test if nothing
   exists yet). If it is too big, split it on the list and take the
   smallest part.
2. Assert First, with Evident Data. One behavior per test. The name says
   what it demonstrates.
3. Isolated Test.
4. Run the whole suite. The new test must fail, and you must be able to
   say why. Not compiling is a valid failure. If the new test passes,
   either it records existing behavior, in which case keep it as a
   Regression Test and pick another item, or the code is doing more than
   its tests say. Check which before moving on; a passing new test has
   found a bug this way.
5. Do not touch production code. Not a stub, not a signature.
6. Assert observable behavior in the problem's words, not an
   implementation you have in mind.
7. Check off the item. Add anything you discovered.

If the list is empty, write `done` to the baton, make the final journal
entry, and stop. The human decides whether the list was finished.

### Hand off

Append the journal entry, then write your partner's role to the baton. In
that order. Then Wait.

## The first turn

`ping` only:

1. If `$ARGUMENTS` has a task statement, write it verbatim to
   `.real-tdd/task.md`. Otherwise read the one there. If there is none,
   ask the human.
2. Write `.real-tdd/test-list.md`: the behaviors the finished code should
   have, in the problem's words. Not steps, not functions.
3. Read the task again, line by line, against the list. Every sentence of
   the task that states a behavior has an item, and no item contradicts a
   sentence. This list will be treated as binding by both sessions for the
   rest of the run.
4. If no test can run yet, add the minimum that lets one test file
   execute. No production code.
5. Commit the scaffold on its own, if there is one. Do the Red step,
   leave the test uncommitted, and hand off to `pong`.

`pong` starts at Wait.

## Rules for both sessions

- No plan. Do not write, anywhere, how the code will be structured.
- The journal reports. It does not tell your partner what to write or how
  to pass what you wrote. The only instruction between sessions is a test.
- One test at a time. Never two reds. Never a test and its implementation
  in the same turn.
- Whole suite, every run.
- One commit per green, and only on green.
- Never read the other session's transcript.

## Journal entry format

Take the timestamp from `date -u`; do not write it from memory.

```markdown
## Turn N — <role> — <output of date -u>

**Received:** <test name> failing because <reason as observed>
**Green by:** Fake It | Obvious Implementation | Triangulate — <one line on why>
**Refactored:** <what duplication was removed, or "nothing">
**Commit:** <hash>
**Also satisfied:** <list items this green covered without a test, or "none">
**Wrote:** <new test name> — fails because <observed reason>
**Interface decided:** <any signature, type, or name this test fixed, or "none">
**List:** <items checked, items added>
**Surprise:** <what the test or the code taught you, or "none">
```

The Surprise line is the point. Write "none" when there was none.
