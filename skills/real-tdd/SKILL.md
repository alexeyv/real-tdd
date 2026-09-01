---
name: real-tdd
description: Kent Beck's test-driven development, as he wrote it, run as ping-pong pairing between two isolated Claude Code sessions sharing one working tree. Use when the user says /real-tdd, "real TDD", or "ping-pong TDD". Requires a partner session; never simulate the partner.
---

# Real TDD

## Statement of intent

This is an honest experiment, not a parody.

Test-driven development as Kent Beck described it is a design technique
with a specific rhythm: write one small failing test, make it pass by the
cheapest means available, remove the duplication that the cheap means
created, repeat. The claim is that the sequence of tests, each one written
before you know how you will pass it, shapes the interface, and that
removing duplication shapes the implementation. The claim is not that you
end up with tests.

Most "TDD for agents" skills keep the vocabulary and drop the mechanism.
They hand the agent a test and the implementation in the same plan, or
have one context write both in the same breath. A test cannot push back on
a design that was decided four seconds earlier by the same mind.

The one thing that made the technique work for humans, that the author of
the test does not yet know the implementation, is impossible inside a
single language-model context and trivially available across two. So this
skill runs the technique across two sessions that share a working tree and
nothing else, in the ping-pong form of pair programming: one session writes
a failing test, the other makes it pass and writes the next failing test,
and the keyboard changes hands on every red.

The question the experiment asks is whether, under those conditions, the
tests drive anything. Whether the interface that emerges differs from what
one session would have written from the task statement in a single pass.
Whether the test list changes during the run, which would mean the
sequence taught somebody something. What it costs. The journal each
session keeps is the data. Nothing in this file assumes the answer.

Everything below that is a rule comes from Beck's *Test-Driven
Development: By Example* (2002) or his *Canon TDD* post (2023), with the
source noted. The ping-pong handoff is an XP community practice, not from
the book. See `references/beck.md` for the sources. Where this skill has to
invent mechanics that Beck never needed, such as who holds the keyboard
when the pair cannot see each other, it says so.

## Invocation

```
/real-tdd ping <task statement>     # first session, starts the run
/real-tdd ping                      # first session, task already in .real-tdd/task.md
/real-tdd pong                      # second session, joins the run
```

Run both sessions in the same repository, in separate terminals. Start
`ping` first. Your role for this run is the first word of `$ARGUMENTS`;
the rest, if present, is the task statement.

If you were invoked and cannot find a partner (no second session will be
started, or the human asks you to play both sides), stop and say so. Do
not simulate the partner with a subagent, a fork, or your own reasoning.
The experiment measures what happens when the test author does not know
the implementation. One context playing both roles knows both, and the
data would be worthless.

## Shared state

All coordination lives in `.real-tdd/` in the repository root, and in the
working tree itself. The sessions never read each other's transcripts.
The working tree is the shared screen; the journal is the talking.

| File | Meaning |
|------|---------|
| `.real-tdd/task.md` | The task, in the human's words. Written once by `ping`. Read-only after. |
| `.real-tdd/test-list.md` | Beck's test list. Behaviors to cover, as checkboxes. Either session may add items at any time. |
| `.real-tdd/baton` | Whose keyboard it is: `ping`, `pong`, or `done`. |
| `.real-tdd/journal.md` | One entry per turn, appended by whoever held the keyboard. The experiment's record. |

## The turn

Whoever's name is in the baton holds the keyboard. Everyone else waits.

### Wait

```bash
until [ "$(cat .real-tdd/baton 2>/dev/null)" = "<your role>" ]; do sleep 5; done
```

If the tool times out, run it again. If the baton reads `done`, the run
is over; read the final journal entry and stop.

### Receive

1. Read the last journal entry, the test list, and `git status`.
2. Run the whole test suite. Expect exactly one failing test: the one your
   partner just wrote. It is uncommitted; the diff is your assignment.
3. Read the failure. Beck's rhythm has you *see the new one fail*, and it
   is your only information about what your partner wants. If it fails for
   a reason that looks like a mistake in the test rather than a missing
   behavior (a typo, a wrong import), fix the test only enough to make it
   fail for the right reason, and say so in the journal. Do not change
   what it asserts.
4. If the failing test is one you wrote yourself, your partner handed it
   back: the journal will say the step was too big or that the test
   contradicts the task. Skip Green and Refactor. Your move is the Red
   step: split the test into a smaller one (Beck's Child Test), rewrite
   it, or withdraw it and pick another item. Then hand off again.

### Green

Make the failing test pass, and keep every other test passing. Beck gives
three ways and says to choose by how confident you are (*TDD by Example*,
Part III, Green Bar Patterns):

- **Fake It.** Return a constant. The constant duplicates the expected
  value in the test. That duplication is what the refactor step removes,
  and removing it is how the real implementation appears. Use this when
  you are not sure.
- **Obvious Implementation.** If the real code is obvious, type it. If the
  bar goes red unexpectedly while you do, back off to Fake It and take
  smaller steps. Step size is a dial, not a rule.
- **Triangulate.** Generalize only when two or more tests demand it. Use
  this when you genuinely do not see the abstraction; otherwise it is
  slow.

Commit whatever sins are necessary to get to green. This is the step where
Beck permits ugliness on purpose. Do not write code the current tests do
not demand; if you see something that will be needed, add it to the test
list and leave it there.

If you cannot get to green in three attempts, revert to the last green
state, write in the journal that the step was too big, and hand the baton
back with the same test still red. Your partner's move is then to split
it (Beck's Child Test) or replace it with a smaller one.

### Refactor

Only on green. Remove duplication, including duplication between the test
and the code you just wrote. Improve names. Do not add behavior. Run all
tests after every change and stay green. This is where Beck says the
implementation design happens, so do not skip it because the code is
small.

When the tree is green and clean, commit it with a conventional-commit
subject. Beck's Clean Check-in: never hand over a red suite except for the
one test you write next.

### Red

Now write the next failing test. This is the half that is interface
design, so it has the most rules.

1. **Pick one item** from the test list. Beck's One Step Test: choose one
   that will teach you something and that you are confident you can
   implement. Early in a run, prefer the Starter Test, something trivial
   that establishes where the code lives and how it is called. If the item
   is too big, split it into smaller items on the list and pick the
   smallest.
2. **Assert First.** Write the assertion, then work backward to the setup
   the assertion needs. Use literal, evident data. One behavior per test;
   the test name says what it demonstrates.
3. **Isolated Test.** The new test must not depend on any other test's
   state or ordering.
4. **Run the whole suite.** The new test must fail, and you must be able to
   say why it failed. "It does not compile" is an acceptable red; Beck
   says so explicitly. A new test that passes is not a step. Either you
   are testing existing behavior, in which case delete it or keep it as a
   Regression Test and pick a different item, or the previous green did
   more than its test demanded.
5. **Do not touch production code.** Not a stub, not a signature, not a
   comment describing the intended implementation. If the test cannot even
   reference the code under test, that is a compile-error red and it is
   your partner's problem to resolve.
6. **Do not write the test to an implementation.** Assert observable
   behavior in the problem's vocabulary. You do not know how your partner
   will pass it, and you are not supposed to.
7. **Update the list.** Check off the item you just turned into a test.
   Add anything you discovered. Beck writes the list at the start and
   keeps adding to it as items appear; the list is the only place a
   future behavior is allowed to live before its test exists.

If the list is empty when you come to pick an item, do not invent one.
Beck's stopping rule is that you write tests until fear turns into
boredom. Write `done` to the baton, make the final journal entry, and
stop. The human decides whether the list was really finished.

### Hand off

Append a journal entry (format below), then write your partner's role to
the baton. Do it in that order; the baton flip is the only signal your
partner gets. Then go back to Wait.

## The first turn

The `ping` session starts the run and does less than a normal turn:

1. If `$ARGUMENTS` carries a task statement, write it verbatim to
   `.real-tdd/task.md`. Otherwise read the one that is there. If there is
   none, ask the human.
2. Write `.real-tdd/test-list.md`. This is Canon TDD step 1: a list of the
   behaviors the finished code should exhibit, in the language of the
   problem, not a list of steps and not a list of functions. Write it
   before writing any test. Stop adding items when the remaining ones
   bore you.
3. If no test can run at all yet, add the minimum scaffold that lets one
   test file execute: a test runner configuration, an empty package. No
   production code.
4. Do the Red step above, then hand off to `pong`.

The `pong` session starts at Wait.

## Rules that apply to both sessions all the time

- **No plan.** Do not write, in any file or in the journal, a description
  of how the code will be structured. The structure is supposed to come
  out of the tests and the refactoring. If you already know the structure,
  the experiment is measuring whether the technique can get there without
  you; let it try.
- **The journal reports, it does not instruct.** Say what you did, which
  green strategy you chose and why, what you refactored, what surprised
  you, what you added to the list. Do not tell your partner what test to
  write next or how to pass the one you wrote. The only instruction one
  session may give the other is a test.
- **Tests are the specification.** If a test you receive asserts something
  that contradicts `task.md`, say so in the journal and hand the baton
  back without a green. Do not silently pass a test you believe is wrong,
  and do not silently change it.
- **One test at a time.** Never two reds. Never a test and its
  implementation in the same turn. If you notice you have written
  production code while holding the Red step, delete it.
- **Whole suite, every time.** Beck runs all the tests, not the new one.
- **Small commits, only on green.** One commit per green-and-refactor.
- **Never read the other session's transcript**, even if the human offers.

## Journal entry format

```markdown
## Turn N — <role> — <ISO timestamp>

**Received:** <test name> failing because <reason as observed>
**Green by:** Fake It | Obvious Implementation | Triangulate — <one line on why>
**Refactored:** <what duplication was removed, or "nothing">
**Commit:** <hash>
**Wrote:** <new test name> — fails because <observed reason>
**List:** <items checked, items added>
**Surprise:** <anything the test or the code taught you, or "none">
```

The Surprise line is the point of the experiment. Fill it honestly, and
write "none" when there was none.
