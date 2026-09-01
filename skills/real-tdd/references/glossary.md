# Glossary

The terms the skill uses, with the meaning both sessions must share. Terms
marked (Beck) are his; the rest are XP community usage or this skill's own.

**Test list** (Beck). A written list of the behaviors the finished code
should have, in the language of the problem, made before the first test and
added to whenever a new behavior comes to mind. Items are crossed off as
they become tests. The list is the only place a behavior may live before its
test exists.

**Red** (Beck). Write one small test that fails. A test that does not
compile counts as failing. Read the failure and be able to say why it
failed.

**Green** (Beck). Change the code so the new test and every earlier test
pass, by the quickest means you have. Ugliness is allowed here on purpose.

**Refactor** (Beck). With every test green, remove the duplication that
getting to green created, including duplication between a test's expected
value and a constant in the code. Do not add behavior. Rerun all tests
after each change.

**Fake It** (Beck). Get to green by returning a constant. The constant
duplicates the test's expected value, and removing that duplication in the
Refactor step is what produces the real implementation. Use it when you are
not sure how to write the real thing.

**Obvious Implementation** (Beck). If you know what the real code is, write
it. If an unexpected test goes red while you do, back off to Fake It and
take smaller steps.

**Triangulate** (Beck). Generalize only once two or more tests require it.
Two examples at opposite ends of one axis are enough; a second example that
differs on a different axis will not force the generalization you want.
Use it only when you do not see the abstraction; otherwise it is slow.

**One Step Test** (Beck). When choosing the next test from the list, pick
one that will teach you something and that you are confident you can make
pass. Not the easiest, not the hardest.

**Starter Test** (Beck). A first test so small it settles only where the
code lives and how it is called. Use it when nothing exists yet.

**Child Test** (Beck). When a test turns out too big to pass quickly,
write a smaller test for one part of it, get that green, then bring the
larger test back.

**Assert First** (Beck). Write the assertion before the setup, then work
backward to whatever the assertion needs.

**Evident Data** (Beck). Use literal values in tests, chosen so the reader
can see how the input relates to the expected result.

**Isolated Test** (Beck). No test depends on another test's state or on
the order tests run in.

**Regression Test** (Beck). A test written for a defect after it was found.
It is the test that should have been written in the first place. Also used
here for a test that was written to record behavior already present; that
is a valid test but not a step.

**Clean Check-in** (Beck). Commit only when every test passes. A commit
contains the test and the code that passed it together.

**Do Over** (Beck). When you are lost, throw the uncommitted work away and
return to the last green commit rather than pushing on.

**Ping-pong.** The pairing rhythm this skill runs: one partner writes a
failing test and hands over; the other makes it pass, refactors, commits,
writes the next failing test, and hands back. XP community practice, not
Beck's.

**Baton.** This skill's stand-in for the shared keyboard: the file
`.real-tdd/baton` names whose turn it is, `ping`, `pong`, or `done`.

**Journal.** This skill's stand-in for talking: `.real-tdd/journal.md`,
one entry per turn, reporting what happened. It is the experiment's data.
